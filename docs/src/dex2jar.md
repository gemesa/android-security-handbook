# dex2jar

## Use case

Convert .dex to .jar, then run parts (e.g. decryption functions) of the app on the host PC.

## Explanation

See [dex2jar](https://github.com/ThexXTURBOXx/dex2jar).

## Usage

```
$ cd test/test-app
$ ./gradlew assembleDebug
$ cd ../..
$ cp test/test-app/app/build/outputs/apk/debug/app-debug.apk .
$ d2j-dex2jar.sh app-debug.apk -o app-debug.jar
dex2jar app-debug.apk -> app-debug.jar
$ javap -cp app-debug.jar -p com.example.test.TextCipher
public class com.example.test.TextCipher {
  private static final byte KEY;
  public com.example.test.TextCipher();
  public static java.lang.String decrypt(java.lang.String);
  public static java.lang.String encrypt(java.lang.String);
  private static byte[] xor(byte[]);
}
$ java -cp app-debug.jar docs/src/scripts/dex2jar/TextCipherReflectionRunner.java 
Exception in thread "main" java.lang.VerifyError: Expecting a stackmap frame at branch target 29
Exception Details:
  Location:
    com/example/test/TextCipher.xor([B)[B @10: if_icmpge
  Reason:
    Expected stackmap frame at this location.
  Bytecode:
    0000000: 2bbe bc08 4e03 3d1c 2bbe a200 132d 1c2b
    0000010: 1c33 105a 8291 5484 0201 a7ff ed2d b0  

	at java.base/java.lang.Class.forName0(Native Method)
	at java.base/java.lang.Class.forName(Class.java:467)
	at java.base/java.lang.Class.forName(Class.java:458)
	at TextCipherReflectionRunner.main(TextCipherReflectionRunner.java:6)
$ java -noverify -cp app-debug.jar docs/src/scripts/dex2jar/TextCipherReflectionRunner.java
OpenJDK 64-Bit Server VM warning: Options -Xverify:none and -noverify were deprecated in JDK 13 and will likely be removed in a future release.
Ej82NjV6PCg1N3ouMj96GwoRew==
Hello from the APK!
```

```java
{{#include scripts/dex2jar/TextCipherReflectionRunner.java}}
```
