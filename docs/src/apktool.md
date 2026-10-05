# `apktool`

## Use case

Unpack and repack the APK.

## Explanation

Decode an APK's resources and disassemble the [Dalvik bytecode](https://source.android.com/docs/core/runtime/dalvik-bytecode) into [smali](https://github.com/google/smali):

- read resources (e.g. `AndroidManifest.xml`)
- read or edit the smali disassembly
- rebuild the modified APK

## Usage

```
$ apktool d test/test-app/app/build/outputs/apk/debug/app-debug.apk -o app-debug
I: Using Apktool 3.0.3 on app-debug.apk with 8 threads
I: Baksmaling classes2.dex...
I: Baksmaling classes.dex...
I: Baksmaling classes4.dex...
I: Baksmaling classes5.dex...
I: Baksmaling classes3.dex...
I: Loading resource table...
I: Decoding value resources...
I: Loading resource table from file: /home/gemesa/.local/share/apktool/framework/1.apk
I: Decoding file resources...
I: Generating values XMLs...
I: Decoding AndroidManifest.xml with resources...
I: Copying original files...
I: Copying assets...
I: Copying unknown files...
$ grep '<service' app-debug/AndroidManifest.xml
        <service android:name="com.example.test.Worker1" android:process=":worker1"/>
        <service android:name="com.example.test.Worker2" android:process=":worker2"/>
$ cat app-debug/smali_classes3/com/example/test/Worker1.smali    
.class public Lcom/example/test/Worker1;
.super Lcom/example/test/TestService;
.source "Worker1.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 3
    invoke-direct {p0}, Lcom/example/test/TestService;-><init>()V

    return-void
.end method
$ apktool b app-debug -o app-debug-patched.apk
I: Using Apktool 3.0.3 on app-debug.apk with 8 threads
I: Smaling smali folder into classes.dex...
I: Smaling smali_classes3 folder into classes3.dex...
I: Smaling smali_classes2 folder into classes2.dex...
I: Smaling smali_classes4 folder into classes4.dex...
I: Smaling smali_classes5 folder into classes5.dex...
I: Building resources with aapt2...
I: Building apk file...
I: Importing assets...
I: Importing unknown files...
I: Built apk into: app-debug-patched.apk
$ keytool -genkeypair -keyalg RSA
$ zipalign -v -p 4 app-debug-patched.apk app-debug-patched-aligned.apk
$ keytool -genkeypair -keyalg RSA -keystore my-release-key.jks -alias mykey
$ apksigner sign --ks my-release-key.jks --out app-debug-patched-aligned-signed.apk app-debug-patched-aligned.apk
$ apksigner verify app-debug-patched-aligned-signed.apk
```

References:

- <https://developer.android.com/build/building-cmdline#sign_manually>
- <https://github.com/ibotpeaches/apktool>
- <http://pallergabor.uw.hu/androidblog/dalvik_opcodes.html>
