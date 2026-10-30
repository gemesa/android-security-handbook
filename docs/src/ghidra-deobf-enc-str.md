# Ghidra

## Use case

Deobfuscate encrypted strings with [emulator](https://ghidra.re/ghidra_docs/api/ghidra/app/emulator/EmulatorHelper.html).

## Usage

Script Manager --> Manage Script Directories --> add/enable `$USER_HOME/ghidra_scripts`

```
$ cp emu-enc-str.py $HOME/ghidra_scripts/
```

```
emu-enc-str.py> Running...
0x130be9: decrypted string: "secret"
0x130bf0: decrypted string: "hidden"
emu-enc-str.py> Finished!
```

```c
{{#include scripts/ghidra/enc-str/test_enc_str.c}}
```

```sh
{{#include scripts/ghidra/enc-str/build.sh}}
```

```py
{{#include scripts/ghidra/enc-str/emu-enc-str.py}}
```
