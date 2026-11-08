# stackplz

## Use case

eBPF-based stack tracing tool. Supports both native and Java stacks.

## Explanation

See [stackplz](https://github.com/SeeFlowerX/stackplz) and [medium.com](https://medium.com/@axhlzy/android-reverse-engineering-basics-syscalls-and-inline-assembly-27587365f329).

## Usage

Add to `.zshrc`:

```
# stackplz
export PATH=$PATH:$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/linux-x86_64/bin/
```

```
$ git clone https://github.com/SeeFlowerX/ebpf
$ git clone https://github.com/SeeFlowerX/ebpfmanager
$ git clone https://github.com/gemesa/stackplz
$ cd stackplz
$ git switch dev-gemesa
$ sudo dnf install golang
$ make
$ chmod +x bin/stackplz_arm64
$ adb push bin/stackplz_arm64 /data/local/tmp/stackplz
```

```
$ test/test-app
$ ./gradlew assembleDebug
$ adb install app/build/outputs/apk/debug/app-debug.apk
$ apkanalyzer manifest application-id app/build/outputs/apk/debug/app-debug.apk        
com.example.test
```

```
$ adb shell
bluejay:/ $ su
bluejay:/ # cd /data/local/tmp
bluejay:/data/local/tmp # ./stackplz -n com.example.test -s openat:f0 --stack -f w:/stackplz_marker
[*] save maps to maps_24175.txt
[*] save maps to maps_24204.txt
[*] save maps to maps_24206.txt
config file -> user/config/config_syscall_aarch64.json
hook syscall count:1
ConfigMap{stackplz_pid=2547,thread_whitelist=0}
uid => whitelist:[10299];blacklist:[]
pid => whitelist:[24175,24204,24206];blacklist:[]
tid => whitelist:[];blacklist:[]
start 2 modules
[24175|24175|om.example.test] openat(dirfd=-100, *pathname=0x77287b05e7(/stackplz_marker), flags=0x0, mode=0o000) LR:0x79f58ae7a8 PC:0x79f5908b88 SP:0x7fc37391c0, Backtrace:
  #00 pc 00000000000e8b88  /apex/com.android.runtime/lib64/bionic/libc.so (__openat+8)
  #01 pc 000000000008e7a4  /apex/com.android.runtime/lib64/bionic/libc.so (__openat_2+68)
  #02 pc 000000000000088c  /data/app/~~pneqkkELYGHetfvFMZCW-g==/com.example.test-5CD7uQXiiN-t6u6JdHOYIg==/base.apk!libnative-lib.so (offset 0xcb4000) (do_probe()+56)
  #03 pc 00000000000008d0  /data/app/~~pneqkkELYGHetfvFMZCW-g==/com.example.test-5CD7uQXiiN-t6u6JdHOYIg==/base.apk!libnative-lib.so (offset 0xcb4000) (Java_com_example_test_Test_probe+20)
  #04 pc 0000000000288270  /apex/com.android.art/lib64/libart.so (art_quick_generic_jni_trampoline+144)
  #05 pc 0000000000270fc0  /apex/com.android.art/lib64/libart.so (art_quick_invoke_static_stub+640)
  #06 pc 00000000006a4f50  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+2484)
  #07 pc 000000000047cc38  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+684)
  #08 pc 000000000048d438  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8)
  #09 pc 0000000000001154  /data/app/~~pneqkkELYGHetfvFMZCW-g==/com.example.test-5CD7uQXiiN-t6u6JdHOYIg==/base.apk
  #10 pc 00000000006a4f0c  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+2416)
  #11 pc 000000000047cc38  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+684)
  #12 pc 000000000048d438  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8)
  #13 pc 0000000000000f7c  /data/app/~~pneqkkELYGHetfvFMZCW-g==/com.example.test-5CD7uQXiiN-t6u6JdHOYIg==/base.apk
  #14 pc 00000000006a4f0c  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+2416)
  #15 pc 000000000047cc38  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+684)
  #16 pc 000000000048d438  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+8)
  #17 pc 0000000000000ed8  /data/app/~~pneqkkELYGHetfvFMZCW-g==/com.example.test-5CD7uQXiiN-t6u6JdHOYIg==/base.apk
  #18 pc 000000000048c844  /apex/com.android.art/lib64/libart.so (artQuickToInterpreterBridge+1216)
  #19 pc 00000000002883a8  /apex/com.android.art/lib64/libart.so (art_quick_to_interpreter_bridge+88)
  #20 pc 000000000246c840  /memfd:jit-cache (deleted) (offset 0x2000000)

[24175|24175|om.example.test] openat(dirfd=-100, *pathname=0x77287b05e7, flags=0x0, mode=0o000, ret=-2)
```
