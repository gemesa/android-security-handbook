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

TODO: run the binary

## Code

```rust
{{#include ../../src/dumpmem/src/main.rs}}
```

[View on GitHub](https://github.com/gemesa/android-security-handbook/blob/main/src/dumpmem/src/main.rs).
