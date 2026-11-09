# Ghidra

## Use case

Deobfuscate [omvll](https://github.com/open-obfuscator/o-mvll/blob/main/src/passes/string-encoding/StringEncoding.cpp) encrypted strings with [emulator](https://ghidra.re/ghidra_docs/api/ghidra/app/emulator/EmulatorHelper.html).

## Usage

Prereqs: build an [obfuscated APK](./o-mvll.md#usage).

Script Manager --> Manage Script Directories --> add/enable `$USER_HOME/ghidra_scripts`

```
$ cp emu-enc-str.py $HOME/ghidra_scripts/
$ cp test/test-app/app/build/outputs/apk/release/app-release-unsigned.apk .
$ apktool d app-release-unsigned.apk
```

```
emu-enc-str.py> Running...
0x1088c0: decrypted string: "Hello from JNI !  Compiled with ABI arm64-v8a."
emu-enc-str.py> Finished!
```

```py
{{#include scripts/ghidra/enc-str-omvll/emu-enc-str.py}}
```

Alternatively, the encrypted data can be decrypted in-place.

```
emu-enc-str-overwrite.py> Running...
0x1088c0: decrypted string: "Hello from JNI !  Compiled with ABI arm64-v8a."
emu-enc-str-overwrite.py> Finished!
```

```py
{{#include scripts/ghidra/enc-str-omvll/emu-enc-str-overwrite.py}}
```

Before:

```
                             //
                             // .data
                             // SHT_PROGBITS  [0x88c0 - 0x88ee]
                             // ram:001088c0-ram:001088ee
                             //
                             
                             DAT_001088c0                                    XREF[4]:     001000f8(*), _INIT_0:00100654(R), 
                                                                                          _INIT_0:00100664(W), 
                                                                                          _elfSectionHeaders::00000550(*)  
        001088c0 21              undefin    21h
                             
                             DAT_001088c1                                    XREF[2]:     _INIT_0:00100654(R), 
                                                                                          _INIT_0:00100664(W)  
        001088c1 0a              undefin    0Ah
        001088c2 04              ??         04h
        001088c3 d7              ??         D7h
        001088c4 30              ??         30h    0
        001088c5 9d              ??         9Dh
        001088c6 23              ??         23h    #
        001088c7 50              ??         50h    P
        001088c8 06              ??         06h
        001088c9 02              ??         02h
        001088ca 48              ??         48h    H
        001088cb f1              ??         F1h
        001088cc 11              ??         11h
        001088cd f4              ??         F4h
        001088ce 65              ??         65h    e
        001088cf 03              ??         03h
        001088d0 49              ??         49h    I
        001088d1 4f              ??         4Fh    O
        001088d2 2b              ??         2Bh    +
        001088d3 d4              ??         D4h
        001088d4 32              ??         32h    2
        001088d5 cd              ??         CDh
        001088d6 2c              ??         2Ch    ,
        001088d7 4e              ??         4Eh    N
        001088d8 0c              ??         0Ch
        001088d9 0b              ??         0Bh
        001088da 48              ??         48h    H
        001088db cc              ??         CCh
        001088dc 36              ??         36h    6
        001088dd c9              ??         C9h
        001088de 2d              ??         2Dh    -
        001088df 02              ??         02h
        001088e0 28              ??         28h    (
        001088e1 2d              ??         2Dh    -
        001088e2 21              ??         21h    !
        001088e3 9b              ??         9Bh
        001088e4 3e              ??         3Eh    >
        001088e5 cf              ??         CFh
        001088e6 28              ??         28h    (
        001088e7 14              ??         14h
        001088e8 5d              ??         5Dh    ]
        001088e9 42              ??         42h    B
        001088ea 1e              ??         1Eh
        001088eb 83              ??         83h
        001088ec 3e              ??         3Eh    >
        001088ed 93              ??         93h
        001088ee 45              ??         45h    E
```

After:

```
                             //
                             // .data
                             // SHT_PROGBITS  [0x88c0 - 0x88ee]
                             // ram:001088c0-ram:001088ee
                             //
                             
                             DAT_001088c0                                    XREF[4]:     001000f8(*), _INIT_0:00100654(R), 
                                                                                          _INIT_0:00100664(W), 
                                                                                          _elfSectionHeaders::00000550(*)  
        001088c0 48              undefin    48h
                             
                             DAT_001088c1                                    XREF[2]:     _INIT_0:00100654(R), 
                                                                                          _INIT_0:00100664(W)  
        001088c1 65              undefin    65h
        001088c2 6c              ??         6Ch    l
        001088c3 6c              ??         6Ch    l
        001088c4 6f              ??         6Fh    o
        001088c5 20              ??         20h     
        001088c6 66              ??         66h    f
        001088c7 72              ??         72h    r
        001088c8 6f              ??         6Fh    o
        001088c9 6d              ??         6Dh    m
        001088ca 20              ??         20h     
        001088cb 4a              ??         4Ah    J
        001088cc 4e              ??         4Eh    N
        001088cd 49              ??         49h    I
        001088ce 20              ??         20h     
        001088cf 21              ??         21h    !
        001088d0 20              ??         20h     
        001088d1 20              ??         20h     
        001088d2 43              ??         43h    C
        001088d3 6f              ??         6Fh    o
        001088d4 6d              ??         6Dh    m
        001088d5 70              ??         70h    p
        001088d6 69              ??         69h    i
        001088d7 6c              ??         6Ch    l
        001088d8 65              ??         65h    e
        001088d9 64              ??         64h    d
        001088da 20              ??         20h     
        001088db 77              ??         77h    w
        001088dc 69              ??         69h    i
        001088dd 74              ??         74h    t
        001088de 68              ??         68h    h
        001088df 20              ??         20h     
        001088e0 41              ??         41h    A
        001088e1 42              ??         42h    B
        001088e2 49              ??         49h    I
        001088e3 20              ??         20h     
        001088e4 61              ??         61h    a
        001088e5 72              ??         72h    r
        001088e6 6d              ??         6Dh    m
        001088e7 36              ??         36h    6
        001088e8 34              ??         34h    4
        001088e9 2d              ??         2Dh    -
        001088ea 76              ??         76h    v
        001088eb 38              ??         38h    8
        001088ec 61              ??         61h    a
        001088ed 2e              ??         2Eh    .
        001088ee 00              ??         00h
```
