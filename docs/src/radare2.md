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
$ apktool d test/test-app/app/build/outputs/apk/debug/app-debug.apk -o app-debug
...
$ r2 -q -c 'aaa; afl' app-debug/lib/arm64-v8a/libnative-lib.so | head -5 
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
INFO: Finding function preludes (aap)
INFO: Emulate functions to find computed references (aaef)
INFO: Recovering local variables (afva@@@F)
INFO: Type matching analysis for all functions (aaft)
INFO: Propagate noreturn information (aanr)
INFO: Use -AA or aaaa to perform additional experimental analysis
INFO: Finding xrefs in noncode sections (e anal.in=io.maps.x; aav)
WARN: Skipping aav because base address is zero. Use -B 0x800000 or aav0
0x00000900    1     16 sym.imp.__cxa_finalize
0x00000910    1     16 sym.imp.__cxa_atexit
0x00000920    1     16 sym.imp.__register_atfork
0x00000950    1     16 sym.imp.__openat_2
0x00000960    1     16 sym.imp.close
```

```
$ r2 -q -c 'iE' app-debug/lib/arm64-v8a/libnative-lib.so 
HINT: Relocs not applied, some references may not resolve: use -e bin.relocs.apply=true
nth paddr      vaddr      bind   type size lib name                                        demangled
――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
6   0x000007f0 0x000007f0 GLOBAL FUNC 48       Java_com_example_test_Test_stringFromNative
8   0x00000854 0x00000854 GLOBAL FUNC 104      _Z8do_probev                                do_probe()
9   0x000008bc 0x000008bc GLOBAL FUNC 36       Java_com_example_test_Test_probe
```

References:
- <https://book.rada.re/>
