# Ghidra

## Use case

Disassemble and decompile native binaries.

## Explanation

Analyze a binary and decompile the machine code into pseudocode (similar to C):

- list functions, strings, imports and cross-references
- read the disassembly and the decompiled code
- automate analysis with scripts (headless mode)

## Usage

GUI:

- <https://github.com/NationalSecurityAgency/ghidra/tree/master/GhidraDocs>

PyGhidra headless:

```py
# @runtime PyGhidra

# mkdir -p /tmp/ghidra_projects
# pyghidraRun -H /tmp/ghidra_projects headless -import /path/to/bin -postScript functions.py -scriptPath /path/to/script -deleteProject

import typing
if typing.TYPE_CHECKING:
    from ghidra.ghidra_builtins import *

from itertools import islice

TAG = "## "

def out(msg):
    print(TAG + str(msg))

for f in islice(currentProgram.getFunctionManager().getFunctions(True), 5):
    out(f"{f.getEntryPoint()}: {f.getName()}")
```

```
$ apktool d test/test-app/app/build/outputs/apk/debug/app-debug.apk -o app-debug
...
$ mkdir -p /tmp/ghidra_projects
$ pyghidraRun -H /tmp/ghidra_projects headless -import app-debug/lib/arm64-v8a/libnative-lib.so -postScript functions.py -scriptPath ~/projects -deleteProject | grep -E '^##'
## 00100660: _FINI_1
## 00100670: FUN_00100670
## 00100678: _FINI_0
## 00100680: FUN_00100680
## 00100694: FUN_00100694
```

References:

- <https://ghidra.re/ghidra_docs/api/ghidra/program/flatapi/FlatProgramAPI.html#currentProgram>
- <https://ghidra.re/ghidra_docs/api/ghidra/program/model/listing/Program.html>
- <https://ghidra.re/ghidra_docs/api/ghidra/program/model/listing/Program.html#getFunctionManager()>
