# Redmi note 10 5G rooting guide

## Prerequisites

- Settings --> Xiaomi Account --> log in with Google account
- set a password and make a note of the account ID
- add a phone number at https://account.xiaomi.com/pass/serviceLogin?checkSafePhone=true
- enable dev options: Settings --> About phone --> MIUI version (tap 7 times)
- Settings --> Additional settings --> Developer options: enable OEM unlocking and USB debugging
- insert a SIM, turn Wi-Fi off and mobile data on, then go to Developer options --> Mi Unlock status --> Add account and device, then remove SIM
- add to `/etc/udev/rules.d/51-android.rules`:

```
SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="2717", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="08ed", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0e8d", MODE="0666", GROUP="plugdev"
```

then:
```

$ sudo udevadm control --reload-rules
$ sudo udevadm trigger
```

reference:
```

$ grep -E "^\w+\s*(Google|Xiaomi|MediaTek)" /usr/share/misc/usb.ids
08ed  MediaTek Inc.
0e8d  MediaTek Inc.
18d1  Google Inc.
2717  Xiaomi Inc.
```

- install https://github.com/MiForge/MiUnlockTool (`pipx install miunlock`)
- install https://github.com/ssut/payload-dumper-go

## Unlock the bootloader

```
$ adb reboot bootloader
$ fastboot devices
$ miunlock

How would you like to log in?

  1 - Browser (default)
  2 - Terminal
  3 - QR code

Choose > 2

Xiaomi Account ID, Email, or Phone (ex> +31XXXXXXXXX)
> XXXXXXXXXX
Password> *********

=== 2FA Verification Required ===


Attempts remaining: 5

Code sent to Email successfully.

Check your Email for the code.
Enter code (or type 'r' to resend): XXXXXX

Login successful

Account Region: NL

dataCenterZone: Europe

(Enter to continue, m to change dataCenterZone) > 

[ Ensure your Xiaomi device is in fastboot mode ] < 


Device Codename: camellia


notice: An unlocked device is an easy target for malware which may damage your device or cause financial loss.


The device will clear user data when unlocked


Press 'Enter' to continue — unlock(encryptData)

code: 20036
description: Please unlock 168 hours later. And do not add your account in MIUI again, otherwise you will wait from scratch
$ fastboot reboot
```

## Download the ROM

- check SW version: Settings --> About phone --> MIUI version: 14.0.4.0(TKSEUXM)
- download from: https://miuirom.org/phones/redmi-note-10-5g --> https://miuirom.org/phones/redmi-note-10-5g#EEA
- check if the mirror points to a legit xiaomi link, e.g. bn.d.miui.com
- if fastboot ROM is not available, download recovery ROM instead: `miui_CAMELLIANEEAGlobal_V14.0.4.0.TKSEUXM_7491c725d3_13.0.zip`
- unzip then `payload-dumper-go -p boot payload.bin`

## Finish unlocking (after 168 hours)

```
$ adb reboot bootloader
$ miunlock
```

-  set up the phone, enable dev options

## Magisk

- download APK from https://github.com/topjohnwu/Magisk/releases

```
$ adb push Magisk-v31.1.apk /sdcard/Download/
```

- install the APK via the UI (`adb install` requires dev options --> Install via USB but that requires a SIM card)

```
$ adb push boot.img /sdcard/Download/
```

- Magisk --> Install --> Select and Patch a File --> boot.img

```
$ adb pull /sdcard/Download/magisk_patched-31100_jIweM.img
$ adb reboot bootloader
$ fastboot flash boot magisk_patched-31100_jIweM.img
$ fastboot reboot
```
