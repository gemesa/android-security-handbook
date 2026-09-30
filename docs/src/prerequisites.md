# Prerequisites

## Rust

```
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
$ rustup target add aarch64-linux-android
```

# Android Studio

Download [Android Studio](https://developer.android.com/studio) (`android-studio-quail1-patch2-linux.tar.gz`).

```
$ sudo dnf install zlib.i686 ncurses-libs.i686 bzip2-libs.i686
$ sudo tar -xzf android-studio-quail1-patch2-linux.tar.gz -C /opt/
$ sudo ln -sf /opt/android-studio/bin/studio /usr/local/bin/android-studio
```
Note: check the Android SDK version of your phone and select the linker accordingly (e.g. `aarch64-linux-android36-clang`).

```
$ adb shell getprop ro.build.version.sdk
37
```

```
$ echo 'export ANDROID_HOME=$HOME/Android/Sdk' >> ~/.zshrc
$ echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools' >> ~/.zshrc
$ echo 'export PATH=$PATH:$ANDROID_HOME/emulator' >> ~/.zshrc
$ echo 'export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin' >> ~/.zshrc
$ echo 'export PATH=$PATH:$ANDROID_HOME/build-tools/$(ls $ANDROID_HOME/build-tools | tail -1)' >> ~/.zshrc
$ echo 'export ANDROID_NDK_HOME=$ANDROID_HOME/ndk/$(ls $ANDROID_HOME/ndk | tail -1)' >> ~/.zshrc
$ echo 'export CARGO_TARGET_AARCH64_LINUX_ANDROID_LINKER=$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android36-clang' >> ~/.zshrc
$ source ~/.zshrc
```

After startup install additional tools:
- **More Actions** --> **SDK Manager** --> **SDK Tools**
  - --> **NDK (Side by side)**
  - --> **Android SDK Command-line Tools (latest)**
  - --> **CMake**
