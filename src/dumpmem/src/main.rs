use std::{
    fs::{self, File},
    io::{self, Read, Seek, SeekFrom, Write},
    path::{Path, PathBuf},
    process::exit,
};

use std::sync::atomic::{AtomicI32, Ordering};

use nix::sys::signal::{Signal, kill};
use nix::unistd::Pid;

// https://docs.rs/clap/latest/clap/#example
use clap::Parser;

/// Dump the rw-p memory regions of an Android process.
#[derive(Parser)]
#[command(version, about)]
struct Args {
    /// Package name to dump, e.g. com.example.com.
    #[arg(short, long)]
    package: String,

    /// Output directory. The output is written to <output>/memdump_<pid>/.
    #[arg(short, long, default_value = "/data/local/tmp")]
    output: PathBuf,
}

static STOPPED_PID: AtomicI32 = AtomicI32::new(-1);

// Resume during cleanup whatever happens.
struct Resumer(Pid);
impl Drop for Resumer {
    fn drop(&mut self) {
        println!("Resuming the app...");
        let _ = kill(self.0, Signal::SIGCONT);
        STOPPED_PID.store(-1, Ordering::SeqCst);
    }
}

fn main() {
    let args = Args::parse();
    if let Err(e) = run(&args.package, &args.output) {
        eprintln!("error: {e}");
        exit(1);
    }
}

fn run(name: &str, out_base: &Path) -> io::Result<()> {
    let pid_raw =
        pidof(name)?.ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "app not running?"))?;
    let pid = Pid::from_raw(pid_raw);
    println!("Found PID: {pid_raw}");

    // output0 = <output>/memdump_<pid>/bin/*.bin
    // output1 = <output>/memdump_<pid>/dumpmem.log
    let out = out_base.join(format!("memdump_{pid_raw}"));
    let bin = out.join("bin");
    let log_path = out.join("dumpmem.log");
    fs::create_dir_all(&bin)?;
    let mut log = File::create(&log_path)?;

    // https://crates.io/crates/ctrlc
    // https://doc.rust-lang.org/std/sync/atomic/enum.Ordering.html
    // We use the scrictest option for now (`SeqCst`), just to be sure.
    ctrlc::set_handler(move || {
        let p = STOPPED_PID.load(Ordering::SeqCst);
        if p >= 0 {
            println!("Resuming the app...");
            let _ = kill(Pid::from_raw(p), Signal::SIGCONT);
        }
        // https://man7.org/linux/man-pages/man7/signal.7.html
        // https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html
        // 128 + SIGINT = 130
        exit(130);
    })
    .expect("failed to install Ctrl+C handler");

    STOPPED_PID.store(pid_raw, Ordering::SeqCst);
    let _resumer = Resumer(pid);
    println!("Stopping the app...");
    kill(pid, Signal::SIGSTOP)?;

    let maps = fs::read_to_string(format!("/proc/{pid_raw}/maps"))?;
    // Good practice: use write_all for bytes we already have.
    log.write_all(maps.as_bytes())?;

    println!("Dumping rw-p regions...");
    let mut mem = File::open(format!("/proc/{pid_raw}/mem"))?;

    // 55fc5b37a000-55fc5b425000 rw-p 00000000 00:00 0    [heap]
    // 7fcd00021000-7fcd04000000 ---p 00000000 00:00 0
    // https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.filter_map
    for region in maps.lines().filter_map(parse_region) {
        let (start, end) = region;
        writeln!(log, "{start:x}-{end:x}")?;

        let len = (end - start) as usize;
        let mut buf = vec![0; len];

        // Straight to the region and read it.
        mem.seek(SeekFrom::Start(start))?;
        match mem.read_exact(&mut buf) {
            Ok(()) => {
                let path = bin.join(format!("{start:x}-{end:x}.bin"));
                fs::write(&path, &buf)?;
                writeln!(log, "wrote {len} bytes -> {}", path.display())?;
            }
            Err(e) => {
                writeln!(log, "skip {start:x}-{end:x}: {e}")?;
            }
        }
    }

    writeln!(log, "Done: {}", out.display())?;
    println!("Done: {}", out.display());

    Ok(())
}

fn pidof(name: &str) -> io::Result<Option<i32>> {
    // https://doc.rust-lang.org/std/fs/fn.read_dir.html#examples
    for entry in fs::read_dir("/proc")? {
        let entry = entry?;
        let fname = entry.file_name();
        let Some(pid) = fname.to_str().and_then(|s| s.parse::<i32>().ok()) else {
            continue;
        };

        // argv[0] = package name
        if let Ok(cmdline) = fs::read(format!("/proc/{pid}/cmdline")) {
            let argv0 = cmdline.split(|&b| b == 0).next().unwrap_or(&[]);
            if argv0 == name.as_bytes() {
                return Ok(Some(pid));
            }
        }
    }
    Ok(None)
}

// 55fc5b37a000-55fc5b425000 rw-p 00000000 00:00 0    [heap]
fn parse_region(line: &str) -> Option<(u64, u64)> {
    let mut parts = line.split_whitespace();
    let range = parts.next()?;
    let perms = parts.next()?;
    if perms != "rw-p" {
        return None;
    };
    let (s, e) = range.split_once('-')?;
    let start = u64::from_str_radix(s, 16).ok()?;
    let end = u64::from_str_radix(e, 16).ok()?;
    Some((start, end))
}
