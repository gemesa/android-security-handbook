# obfuscator-llvm

## Use case

Obfuscate native code with LLVM IR level obfuscation passes.

## Explanation

[Maintained version](https://github.com/eshard/obfuscator-llvm) of the original [obfuscator-llvm](https://github.com/obfuscator-llvm/obfuscator).

Supported obfuscation passes:

- [Bogus control flow](https://github.com/eshard/obfuscator-llvm/blob/main/bogus/BogusControlFlow.cpp)
- [CFG flattening](https://github.com/eshard/obfuscator-llvm/blob/main/flattening/Flattening.cpp)
- [Basic block splitting](https://github.com/eshard/obfuscator-llvm/blob/main/split/SplitBasicBlocks.cpp)
- [String encryption](https://github.com/eshard/obfuscator-llvm/blob/main/string/StringObfuscation.cpp)
- [Instruction substitution](https://github.com/eshard/obfuscator-llvm/blob/main/substitution/Substitution.cpp)

## Usage

General:

```
$ git clone git@github.com:llvm/llvm-project.git llvm-project-21
$ git switch release/21.x
$ cmake -S llvm -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DLLVM_PARALLEL_LINK_JOBS=1 -DLLVM_ENABLE_PROJECTS="clang" -DCMAKE_INSTALL_PREFIX=/opt/llvm
$ ninja -C build -j 12
$ sudo ninja install
```

```
$ sudo dnf install xxd
$ git clone https://github.com/eshard/obfuscator-llvm.git
$ cd obfuscator-llvm
$ mkdir -p build && cd build
$ cmake -G "Ninja" -DLLVM_DIR=/opt/llvm/lib/cmake ..
$ ninja -j$(nproc)
```

```
$ sudo dnf install qemu-user-static-aarch64
$ sudo dnf -y --forcearch=aarch64 --installroot=/opt/a64 --releasever=$(rpm -E %fedora) --use-host-config install glibc-devel gcc
$ sudo dnf install lld
```

```sh
{{#include scripts/obfuscator-llvm/build.sh}}
```

```c
{{#include scripts/obfuscator-llvm/test_sub.c}}
```

```
{{#include scripts/obfuscator-llvm/test_sub_a64.ll}}
```

```c
undefined8 main(int param_1,long param_2)

{
  uint uVar1;
  uint uVar2;
  long lVar3;
  
  if (param_1 < 2) {
    uVar1 = 7;
  }
  else {
    lVar3 = strtol(*(char **)(param_2 + 8),(char **)0x0,10);
    uVar1 = (uint)lVar3;
  }
  if (param_1 < 3) {
    uVar2 = 3;
  }
  else {
    lVar3 = strtol(*(char **)(param_2 + 0x10),(char **)0x0,10);
    uVar2 = (uint)lVar3;
  }
  printf("or=%d",((uVar2 ^ 0xffffffff) & 0xef27f53c | uVar2 & 0x10d80ac3) ^
                 ((uVar1 ^ 0xffffffff) & 0xef27f53c | uVar1 & 0x10d80ac3) |
                 (~uVar2 | uVar1 ^ 0xffffffff) ^ 0xffffffff);
  return 0;
}
```

```
{{#include scripts/obfuscator-llvm/test_sub_a64_obf.ll}}
```

Android:

See [ANDROID_NDK.md](https://github.com/eshard/obfuscator-llvm/blob/main/docs/ANDROID_NDK.md).

References:
- https://github.com/eshard/obfuscator-llvm
- https://github.com/za233/Polaris-Obfuscator/tree/main
- https://github.com/Apich-Organization/ensia
