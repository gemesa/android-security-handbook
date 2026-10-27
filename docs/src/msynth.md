# msynth

## Use case

Code deobfuscation framework to simplify Mixed Boolean-Arithmetic (MBA) expressions.

## Explanation

Python framework built on top of [Miasm](https://github.com/cea-sec/miasm).

Supported simplification methods:

- [Oracle-based simplification](https://github.com/mrphrazer/msynth#pre-computed-simplification-lookup-tables) using pre-computed lookup tables
- [Stochastic program synthesis](https://github.com/mrphrazer/msynth#stochastic-program-synthesis) that learns expressions from input-output behavior

## Usage

```
$ git clone https://github.com/mrphrazer/msynth.git
$ cd msynth
$ python -m venv msynth-env
$ source msynth-env/bin/activate
$ pip install -r requirements.txt
$ pip install .
$ unzip -d database -q database/3_variables_constants_7_nodes.txt.zip
```

The test binary is generated with [obfuscator-llvm](https://shadowshell.io/android-security-handbook/obfuscator-llvm.html#usage):

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

```py
from miasm.expression.expression import ExprId, ExprInt
from msynth import Synthesizer

uVar1 = ExprId("uVar1", 32)
uVar2 = ExprId("uVar2", 32)
k = lambda v: ExprInt(v, 32)

e = ((uVar2 ^ k(0xffffffff)) & k(0xef27f53c) | uVar2 & k(0x10d80ac3)) ^ \
    ((uVar1 ^ k(0xffffffff)) & k(0xef27f53c) | uVar1 & k(0x10d80ac3)) | \
    (~uVar2 | uVar1 ^ k(0xffffffff)) ^ k(0xffffffff)

s = Synthesizer()
left, right = e.args
print(s.simplify(s.simplify(left) | s.simplify(right)))
```

```
$ python simplify.py           
uVar1 | uVar2
```

References:
- https://github.com/mrphrazer/msynth/blob/main/scripts/synthesize_expression.py
