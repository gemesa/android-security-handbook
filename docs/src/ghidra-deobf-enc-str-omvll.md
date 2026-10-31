# Ghidra

## Use case

Deobfuscate [omvll](https://github.com/open-obfuscator/o-mvll/blob/main/src/passes/string-encoding/StringEncoding.cpp) encrypted strings with [emulator](https://ghidra.re/ghidra_docs/api/ghidra/app/emulator/EmulatorHelper.html).

## Usage

Script Manager --> Manage Script Directories --> add/enable `$USER_HOME/ghidra_scripts`

```
$ cp emu-enc-str.py $HOME/ghidra_scripts/
$ cp test/test-app/app/build/outputs/apk/release/app-release-unsigned.apk .
$ apktool d app-release-unsigned.apk
```

```
emu-enc-str.py> Running...
0x1088c0: decrypted string: "Hello from JNI !  Compiled with ABI arm64-v8a."
emu-enc-str.py> Finished!
```

```py
{{#include scripts/ghidra/enc-str-omvll/emu-enc-str.py}}
```
