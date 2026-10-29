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
#include <stdio.h>

#define STR_LEN 6

// "secret"
const unsigned char enc_str1[STR_LEN] = {0x29, 0x3f, 0x39, 0x28, 0x3f, 0x2e};
// "hidden"
const unsigned char enc_str2[STR_LEN] = {0x5f, 0x5e, 0x53, 0x53, 0x52, 0x59};

char dec_str1[STR_LEN + 1];
char dec_str2[STR_LEN + 1];

__attribute__((noinline)) void decrypt_str1(char *dst,
                                            const unsigned char *src) {
  for (int i = 0; i < STR_LEN; i++)
    dst[i] = src[i] ^ 0x5A;
  dst[STR_LEN] = '\0';
}

__attribute__((noinline)) void decrypt_str2(char *dst,
                                            const unsigned char *src) {
  for (int i = 0; i < STR_LEN; i++)
    dst[i] = src[i] ^ 0x37;
  dst[STR_LEN] = '\0';
}

int main(void) {
  decrypt_str1(dec_str1, enc_str1);
  decrypt_str2(dec_str2, enc_str2);

  printf("%s\n", dec_str1);
  printf("%s\n", dec_str2);
  return 0;
}
```

```sh
#!/usr/bin/env bash
set -euo pipefail

LLVM=/opt/llvm/bin
PLUGIN=$PWD/../build/libLLVMObfuscator.so
SYSROOT=/opt/a64
T="--target=aarch64-linux-gnu --sysroot=$SYSROOT"

SRC=test_enc_str.c
OUT=test_enc_str_a64

$LLVM/clang $T -fuse-ld=lld -O1 $SRC -o ${OUT}
$LLVM/llvm-strip ${OUT}
```

```py
{{#include scripts/emu-enc-str.py}}
```
