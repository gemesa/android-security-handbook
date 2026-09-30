# Memory dumping

## Use case

Capture the mapped memory of a process to recover values from RAM.

## Explanation

The list of mapped regions is available through `/proc/<pid>/maps`. The content of these regions can be read via `/proc/<pid>/mem`. It is a good idea to freeze the process first, then dump the memory. For now, we only dump `rw-p` regions.

## Usage

Note: check the Android SDK version of your phone and select the linker accordingly.

```
$ adb shell getprop ro.build.version.sdk
37
```

```
$ export CARGO_TARGET_AARCH64_LINUX_ANDROID_LINKER=$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android36-clang
$ cargo build --release --target aarch64-linux-android
$ adb push target/aarch64-linux-android/release/dumpmem /data/local/tmp/
```

Phone:

```
# ./dumpmem -p com.example.app
Found PID: 13538
Stopping the app...
Dumping rw-p regions...
Done: /data/local/tmp/memdump_13538
Resuming the app...
# ls memdump_13538/
bin  dumpmem.log
# ls memdump_13538/bin/ | head -n 5
2000000-12000000.bin
22000000-32000000.bin
60f0f04000-60f0f06000.bin
60f18ef000-60f19eb000.bin
60f2d2a000-60f2d2c000.bin
# head -n 5 memdump_13538/dumpmem.log
02000000-12000000 rw-p 00000000 00:00 0                                  [anon:dalvik-main space]
22000000-32000000 rw-p 00000000 00:00 0                                  [anon:dalvik-free list large object space]
42000000-44000000 r--s 00000000 00:01 1043                               /memfd:jit-zygote-cache (deleted)
44000000-46000000 r-xs 02000000 00:01 1043                               /memfd:jit-zygote-cache (deleted)
46000000-48000000 r--s 00000000 00:01 1528                               /memfd:jit-cache (deleted)
```

## Code

```rust
{{#include ../../src/dumpmem/src/main.rs}}
```

[View on GitHub](https://github.com/gemesa/android-security-handbook/blob/main/src/dumpmem/src/main.rs).
