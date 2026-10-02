# Memory dumping

## Use case

Capture the mapped memory of a process to recover values from RAM.

## Explanation

The list of mapped regions is available through `/proc/<pid>/maps`. The content of these regions can be read via `/proc/<pid>/mem`. It is a good idea to freeze the process first, then dump the memory. For now, we only dump `rw-p` regions.

There are other solutions available for dumping memory, e.g. [hexdump](https://frida.re/docs/javascript-api/#hexdump), [fridump](https://github.com/Nightbringer21/fridump) or [`gdb` and `lldb`](https://lldb.llvm.org/use/map.html#save-binary-memory-data-starting-at-0x1000-and-ending-at-0x2000-to-a-file). The main problem is that attaching to a process with `frida`, `gdb` and `lldb` can be detected.

## Usage

```
$ cargo build --release --target aarch64-linux-android
$ adb push target/aarch64-linux-android/release/dumpmem /data/local/tmp/
```

Phone:

```
# ps -ef | grep test                         
u0_a217       3585   465 0 19:28:56 ?     00:00:01 com.example.test
u0_a217       3604   465 0 19:28:56 ?     00:00:00 com.example.test:worker1
u0_a217       3605   465 0 19:28:56 ?     00:00:00 com.example.test:worker2
# ./dumpmem -p com.example.test
Found PID: 3585
Stopping the app...
Dumping rw-p regions...
Done: /data/local/tmp/memdump_3585
Resuming the app...
# ls memdump_3585 
bin  dumpmem.log
# ls memdump_3585/bin | head -n 5
2000000-e000000.bin
26000000-32000000.bin
4a000000-4a002000.bin
57e9108b0000-57e9108b1000.bin
6ffb4000-702a0000.bin
# head -n 5 memdump_3585/dumpmem.log 
02000000-0e000000 rw-p 00000000 00:00 0                                  [anon:dalvik-main space]
26000000-32000000 rw-p 00000000 00:00 0                                  [anon:dalvik-free list large object space]
4a000000-4a002000 rw-p 00000000 00:00 0 
4a002000-4c002000 r--s 00000000 00:01 1040                               /memfd:jit-zygote-cache (deleted)
4c002000-4e002000 r-xs 02000000 00:01 1040                               [anon_shmem:dalvik-zygote-jit-code-cache]
```

## Code

```rust
{{#include ../../src/dumpmem/src/main.rs}}
```

[View on GitHub](https://github.com/gemesa/android-security-handbook/blob/main/src/dumpmem/src/main.rs).
