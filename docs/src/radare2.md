# radare2

## Use case

Disassemble and analyze native binaries. Good for scripting.

## Explanation

Analyze a binary:

- list functions, strings, imports and cross-references
- read the disassembly
- automate analysis with one-liners

## Usage

GUI:

- <https://github.com/rizinorg/cutter>

CLI:

```
$ r2 -q -c 'aaa; afl' ~/projects/ls | head -5
HINT: Relocs not applied, some references may not resolve: use -e bin.relocs.apply=true
INFO: Analyze all flags starting with sym. and entry0 (aa)
INFO: Analyze imports (af@@@i)
INFO: Name local plt stubs from their got relocs (anal.plt)
INFO: Analyze entrypoint (af@ entry0)
INFO: Analyze symbols (af@@@s)
INFO: Running plugin pre-analysis hooks
INFO: Analyze all functions arguments/locals (afva@@F)
INFO: Analyze function calls (aac)
INFO: Analyze len bytes of instructions for references (aar)
INFO: Finding and parsing C++ vtables (avrr)
INFO: Analyzing methods (af @@ method.*)
INFO: Recovering local variables (afva@@@F)
INFO: Type matching analysis for all functions (aaft)
INFO: Propagate noreturn information (aanr)
INFO: Use -AA or aaaa to perform additional experimental analysis
0x00000a00    1     10 sym.imp.__ctype_toupper_loc
0x00000a10    1     10 sym.imp.getenv
0x00000a20    1     10 sym.imp.cap_to_text
0x00000a30    1     10 sym.imp.sigprocmask
0x00000a40    1     10 sym.imp.__snprintf_chk
```

References:
- <https://book.rada.re/>
