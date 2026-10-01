# Prerequisites

## Rust

```
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
$ rustup target add aarch64-linux-android
```

## yara-x

```
$ cargo install yara-x-cli
```

## udev rules

Adding the udev rules manually might not be necessary on certain distros.

```
$ lsusb
...
Bus 001 Device 067: ID 18d1:4ee7 Google Inc. Nexus/Pixel Device (charging + debug)
...
$ echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", ATTR{idProduct}=="4ee7", MODE="0660", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/51-android.rules
$ sudo usermod -aG plugdev $USER
$ sudo udevadm control --reload
$ sudo udevadm trigger
```

## Android Studio

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

## Emulator

Note: `google_apis_playstore` does not allow `adb root`.

```
$ sdkmanager "system-images;android-36;google_apis;x86_64"
$ avdmanager create avd -n test -k "system-images;android-36;google_apis;x86_64"
$ android emulator list                                                         
test
$ android emulator start test
Emulator process 2673237 started, log file location: '/home/gemesa/.android/test/emulator.log'
Waiting for virtual device 'test' to fully start (242 seconds left)
Virtual device successfully started as 'emulator-5554'
$ adb devices
List of devices attached
emulator-5554	device
$ adb shell getprop ro.build.version.sdk
36
$ adb root
$ adb shell
```
