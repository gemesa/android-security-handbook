# miasm

## Use case

Reverse engineering framework in Python.

## Explanation

See [miasm](https://github.com/cea-sec/miasm) and [miasm.re](https://miasm.re/blog/).

Examples:

- [Assembling / Disassembling](https://github.com/cea-sec/miasm#assembling--disassembling)
- [Emulation](https://github.com/cea-sec/miasm#emulation)
- [Symbolic execution](https://github.com/cea-sec/miasm#symbolic-execution)

## Usage

```
$ pip install miasm
```

```py
{{#include scripts/miasm/simplify.py}}
```

```
$ python simplify.py
0x32A86D
```

References:
- https://github.com/cea-sec/miasm/blob/master/doc/expression/expression.ipynb
- https://github.com/cea-sec/miasm/blob/master/example/expression/simplification_add.py
