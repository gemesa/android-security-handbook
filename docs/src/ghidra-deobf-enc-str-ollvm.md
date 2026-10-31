# Ghidra

## Use case

Deobfuscate [ollvm](https://github.com/eshard/obfuscator-llvm/blob/main/string/StringObfuscation.cpp) encrypted strings with [emulator](https://ghidra.re/ghidra_docs/api/ghidra/app/emulator/EmulatorHelper.html).

## Usage

Script Manager --> Manage Script Directories --> add/enable `$USER_HOME/ghidra_scripts`

```
$ cp emu-enc-str.py $HOME/ghidra_scripts/
```

```
emu-enc-str.py> Running...
0x130a20: decrypted string: "secret"
0x130a27: decrypted string: "hidden"
emu-enc-str.py> Finished!
```

```c
{{#include scripts/ghidra/enc-str-ollvm/test_enc_str.c}}
```

```sh
{{#include scripts/ghidra/enc-str-ollvm/build.sh}}
```

```py
{{#include scripts/ghidra/enc-str-ollvm/emu-enc-str.py}}
```
