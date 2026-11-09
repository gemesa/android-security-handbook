# LIEF

## Use case

Cross-platform library to parse, modify and abstract ELF, PE and MachO formats.

## Explanation

See [LIEF](https://github.com/lief-project/LIEF) and [lief.re](https://lief.re/).

## Usage

```
$ pip install lief
```

```
$ cd test/test-app 
$ ./gradlew assembleDebug
$ apktool d app/build/outputs/apk/debug/app-debug.apk
$ ls app/build/outputs/apk/debug/app-debug/lib/arm64-v8a
libnative-lib.so
$ cp app/build/outputs/apk/debug/app-debug/lib/arm64-v8a/libnative-lib.so .
```

List JNI functions:

```py
{{#include scripts/lief/jni-functions.py}}
```

```
$ python docs/src/scripts/lief/jni-functions.py 
0x7f0 Java_com_example_test_Test_stringFromNative
0x8bc Java_com_example_test_Test_probe
```

Check hardening:

```py
{{#include scripts/lief/hardening.py}}
```

```
$ python docs/src/scripts/lief/hardening.py
PIE: False
NX: True
Canary: False
```

Inject [frida gadget](https://frida.re/docs/gadget/):

```py
{{#include scripts/lief/frida-gadget.py}}
```

```
$ wget https://github.com/frida/frida/releases/download/17.26.2/frida-gadget-17.26.2-android-arm64.so.xz
$ xz -d frida-gadget-17.26.2-android-arm64.so.xz
$ mv frida-gadget-17.26.2-android-arm64.so libgadget.so
$ readelf -d libnative-lib.so | grep NEEDED                                              
 0x0000000000000001 (NEEDED)             Shared library: [libm.so]
 0x0000000000000001 (NEEDED)             Shared library: [libdl.so]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so]
$ python docs/src/scripts/lief/frida-gadget.py
$ readelf -d libnative-lib.so | grep NEEDED   
 0x0000000000000001 (NEEDED)             Shared library: [libgadget.so.so]
 0x0000000000000001 (NEEDED)             Shared library: [libm.so]
 0x0000000000000001 (NEEDED)             Shared library: [libdl.so]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so]
```
