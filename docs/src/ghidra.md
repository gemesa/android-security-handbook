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

### JNI

Android uses the [JNI](https://docs.oracle.com/en/java/javase/21/docs/specs/jni/) to call native functions from the managed code and vice versa. The following chapters are the most important ones to understand the calling convention:

- [Type Signatures](https://docs.oracle.com/en/java/javase/21/docs/specs/jni/types.html#type-signatures)
- [Calling Instance Methods](https://docs.oracle.com/en/java/javase/21/docs/specs/jni/functions.html#calling-instance-methods)
- [Calling Static Methods](https://docs.oracle.com/en/java/javase/21/docs/specs/jni/functions.html#calling-static-methods)

Additionally, we need to retype the parameters passed to the native functions in order to be able to read and understand the native code. For this purpose, we can use [this .gdt file](https://github.com/Ayrx/JNIAnalyzer/blob/7170ce6bd138caa6be702e357b3aeb74231ae12f/JNIAnalyzer/data/jni_all.gdt).

For example, this is what `Java_s_ni_ob` (`ni.ob` on the Java side) looks like with and without the proper types applied.

Before:

```c
void Java_s_ni_ob(_jclass *param_1,undefined4 param_2,_jmethodID *param_3,undefined4 param_4)

{
  _jmethodID *p_Var1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined1 *puVar4;
  
  puVar4 = &stack0xfffffff8;
  p_Var1 = (_jmethodID *)(**(code **)(*(int *)param_1 + 0x18))(param_1,"android/content/Intent");
  uVar2 = (**(code **)(*(int *)param_1 + 0x84))
                    (param_1,p_Var1,"<init>","(Landroid/content/Context;Ljava/lang/Class;)V");
  uVar2 = _JNIEnv::NewObject(param_1,p_Var1,uVar2,param_3,param_4,puVar4);
  uVar3 = (**(code **)(*(int *)param_1 + 0x7c))(param_1,param_3);
  uVar3 = (**(code **)(*(int *)param_1 + 0x84))
                    (param_1,uVar3,"startService",
                     "(Landroid/content/Intent;)Landroid/content/ComponentName;");
  _JNIEnv::CallObjectMethod((_jobject *)param_1,param_3,uVar3,uVar2);
  return;
}
```

After:

```c
void Java_s_ni_ob(JNIEnv *env,jclass clazz,jobject obj,jobject obj2)

{
  jclass p_Var1;
  jmethodID p_Var2;
  undefined4 uVar3;
  undefined1 *puVar4;
  
  puVar4 = &stack0xfffffff8;
  p_Var1 = (*(*env)->FindClass)(env,"android/content/Intent");
  p_Var2 = (*(*env)->GetMethodID)
                     (env,p_Var1,"<init>","(Landroid/content/Context;Ljava/lang/Class;)V");
  uVar3 = _JNIEnv::NewObject((_jclass *)env,(_jmethodID *)p_Var1,p_Var2,obj,obj2,puVar4);
  p_Var1 = (*(*env)->GetObjectClass)(env,obj);
  p_Var2 = (*(*env)->GetMethodID)
                     (env,p_Var1,"startService",
                      "(Landroid/content/Intent;)Landroid/content/ComponentName;");
  _JNIEnv::CallObjectMethod((_jobject *)env,(_jmethodID *)obj,p_Var2,uVar3);
  return;
}
```
