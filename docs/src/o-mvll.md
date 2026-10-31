# obfuscator-llvm

## Use case

Obfuscate native code with LLVM IR level obfuscation passes. Actively maintained by Build38.

## Explanation

Supported obfuscation passes are available [here](https://github.com/open-obfuscator/o-mvll/tree/main/src/passes).

## Usage

```
$ cd test/test-app
$ source ./omvll.env
$ ./gradlew clean assembleRelease
```

```py
{{#include ../../test/test-app/omvll_config.py}}
```

```
{{#include ../../test/test-app/omvll.env}}
```

```
$ cat omvll-logs/omvll-module-logs/aarch64/native-lib.cpp-omvll-128971.log 
[omvll::AntiHook] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::AntiHook] Changes not applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::FunctionOutline] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::StringEncoding] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::StringEncoding] Processing string Hello from JNI !  Compiled with ABI arm64-v8a.
Invoke subprocess: /home/gemesa/Android/Sdk/ndk/29.0.14206865/toolchains/llvm/prebuilt/linux-x86_64/bin/clang-21 -S -emit-llvm -target aarch64-none-linux-android28 -target aarch64-none-linux-android28 -std=c++17 -o /home/gemesa/git-repos/android-security-handbook/test/test-app/cache/omvll-cache-aarch64-none-linux-android28-2a1de4.ll /home/gemesa/git-repos/android-security-handbook/test/test-app/cache/omvll-cache-aarch64-none-linux-android28-2a1de4.cpp 
[omvll::StringEncoding] Changes  applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::OpaqueFieldAccess] Changes not applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::BasicBlockDuplicate] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::BasicBlockDuplicate] Changes not applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::ControlFlowFlattening] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::ControlFlowFlattening] Changes not applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::BasicBlockSplit] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::BasicBlockSplit] Changes not applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::BreakControlFlow] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::OpaqueConstants] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::OpaqueConstants] Changes not applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::Arithmetic] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::Arithmetic] Changes not applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::ShuffleOps] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::ShuffleOps] Changes not applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::IndirectCall] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::IndirectCall] Changes not applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::IndirectBranch] Executing on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
[omvll::IndirectBranch] Changes not applied on module /home/gemesa/git-repos/android-security-handbook/test/test-app/app/src/main/cpp/native-lib.cpp
```
