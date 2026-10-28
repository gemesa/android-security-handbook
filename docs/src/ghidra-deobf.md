# Ghidra

## Use case

On top of the regular static analysis [features](./ghidra.md), Ghidra can be used for certain deobfuscation tasks.

## Explanation

Useful features:

- splitting and initializing blocks in Memory Map (e.g. `.bss`)
- marking data as constant
- emulator

## Usage

### Prerequisites

Script Manager --> Manage Script Directories --> add/enable `$USER_HOME/ghidra_scripts`

### Deobfuscate bogus control flow (bcf)

```
$ cp deobf-bcf.py $HOME/ghidra_scripts/
```

```
deobf-bcf.py> Running...
x    @ 00130db0
y    @ 00130db4
x.1  @ 00130db8
y.2  @ 00130dbc
main: patched 16 opaque branch(es)
deobf-bcf.py> Finished!
```

```py
{{#include scripts/deobf-bcf.py}}
```

Before:

```c
undefined8 main(int param_1,long param_2)

{
  int iVar1;
  int iVar2;
  int param1;
  long lVar3;
  
  do {
    if ((x * (x + -1) & 1U) == 0) break;
  } while (9 < y);
  if (param_1 < 2) {
    iVar1 = 7;
  }
  else {
    if (((x * (x + -1) & 1U) != 0) && (9 < y)) goto LAB_0011087c;
    while( true ) {
      lVar3 = strtol(*(char **)(param_2 + 8),(char **)0x0,10);
      iVar1 = (int)lVar3;
      if (((x * (x + -1) & 1U) == 0) || (y < 10)) break;
LAB_0011087c:
      strtol(*(char **)(param_2 + 8),(char **)0x0,10);
    }
  }
  do {
    if ((x * (x + -1) & 1U) == 0) break;
  } while (9 < y);
  if (param_1 < 3) {
    iVar2 = 3;
  }
  else {
    if (((x * (x + -1) & 1U) != 0) && (9 < y)) goto LAB_00110918;
    while( true ) {
      lVar3 = strtol(*(char **)(param_2 + 0x10),(char **)0x0,10);
      iVar2 = (int)lVar3;
      if (((x * (x + -1) & 1U) == 0) || (y < 10)) break;
LAB_00110918:
      strtol(*(char **)(param_2 + 0x10),(char **)0x0,10);
    }
  }
  do {
    if ((x * (x + -1) & 1U) == 0) break;
  } while (9 < y);
  param1 = iVar1 - iVar2;
  if (param1 == 0 || iVar1 < iVar2) {
    if ((x * (x + -1) & 1U) != 0 && 9 < y) goto LAB_001109c8;
    while ((param1 = mix(iVar1,iVar2), (x * (x + -1) & 1U) != 0 && (9 < y))) {
LAB_001109c8:
      mix(iVar1,iVar2);
    }
  }
  else {
    do {
      if ((x * (x + -1) & 1U) == 0) break;
    } while (9 < y);
  }
  if (((x * (x + -1) & 1U) != 0) && (9 < y)) goto code_r0x00110a24;
  while ((printf("r=%d\n",param1), (x * (x + -1) & 1U) != 0 && (9 < y))) {
code_r0x00110a24:
    printf("r=%d\n",param1);
  }
  return 0;
}
```

![bcf graph before](./res/bcf-graph-before.png)

After:

```c
/* WARNING: Removing unreachable block (ram,0x00110968) */

undefined8 main(int param_1,long param_2)

{
  int iVar1;
  int iVar2;
  int param1;
  long lVar3;
  
  if (param_1 < 2) {
    iVar1 = 7;
  }
  else {
    lVar3 = strtol(*(char **)(param_2 + 8),(char **)0x0,10);
    iVar1 = (int)lVar3;
  }
  if (param_1 < 3) {
    iVar2 = 3;
  }
  else {
    lVar3 = strtol(*(char **)(param_2 + 0x10),(char **)0x0,10);
    iVar2 = (int)lVar3;
  }
  param1 = iVar1 - iVar2;
  if (param1 == 0 || iVar1 < iVar2) {
    param1 = mix(1,iVar1,iVar2);
  }
  printf("r=%d\n",param1);
  return 0;
}
```

![bcf graph after](./res/bcf-graph-after.png)
