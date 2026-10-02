# Test app

## Use case

This app can be used to test tools such as:

- [`dumpmem`](./memory-dumping.md)
- [`mkrule`](./memory-search.md)

## Usage

```
$ cd test/test-app
$ ./gradlew assemble
$ adb install app/build/outputs/apk/debug/app-debug.apk
$ adb shell am start -n com.example.test/.MainActivity
$ adb shell ps -ef | grep test                         
u0_a217       3585   465 0 19:28:56 ?     00:00:01 com.example.test
u0_a217       3604   465 0 19:28:56 ?     00:00:00 com.example.test:worker1
u0_a217       3605   465 0 19:28:56 ?     00:00:00 com.example.test:worker2
```
