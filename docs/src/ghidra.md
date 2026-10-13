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
$ mkdir -p /tmp/ghidra_projects
$ pyghidraRun -H /tmp/ghidra_projects headless -import ~/projects/ls -postScript functions.py -scriptPath ~/projects -deleteProject | grep -E '^##'
## 0010033c: _init
## 00100a00: __ctype_toupper_loc
## 00100a10: getenv
## 00100a20: cap_to_text
## 00100a30: sigprocmask
```

References:

- <https://ghidra.re/ghidra_docs/api/ghidra/program/flatapi/FlatProgramAPI.html#currentProgram>
- <https://ghidra.re/ghidra_docs/api/ghidra/program/model/listing/Program.html>
- <https://ghidra.re/ghidra_docs/api/ghidra/program/model/listing/Program.html#getFunctionManager()>
