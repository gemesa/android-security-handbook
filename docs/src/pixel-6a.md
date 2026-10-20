# Pixel 6a rooting guide

## Prerequisites

- enable the following in developer options:
   - OEM unlocking
   - USB debugging
- check: Settings --> ABout phone --> Build number: CP3A.261005.002.A1
  - https://developers.google.com/android/images#bluejay
  - `wget https://dl.google.com/dl/android/aosp/bluejay-cp3a.261005.002.a1-factory-79d88414.zip`

```
$ adb reboot bootloader
$ fastboot flashing unlock
```

```
$ unzip bluejay-cp3a.261005.002.a1-factory-79d88414.zip                
Archive:  bluejay-cp3a.261005.002.a1-factory-79d88414.zip
   creating: bluejay-cp3a.261005.002.a1/
 extracting: bluejay-cp3a.261005.002.a1/image-bluejay-cp3a.261005.002.a1.zip  
  inflating: bluejay-cp3a.261005.002.a1/bootloader-bluejay-bluejay-17.0-15681480.img  
  inflating: bluejay-cp3a.261005.002.a1/radio-bluejay-g5123b-145971-260721-b-15910359.img  
  inflating: bluejay-cp3a.261005.002.a1/flash-all.bat  
  inflating: bluejay-cp3a.261005.002.a1/d3m2.ec.bin  
  inflating: bluejay-cp3a.261005.002.a1/proto11.ec.bin  
  inflating: bluejay-cp3a.261005.002.a1/evt.ec.bin  
  inflating: bluejay-cp3a.261005.002.a1/flash-base.sh  
  inflating: bluejay-cp3a.261005.002.a1/flash-all.sh
$ cd bluejay-cp3a.261005.002.a1
$ unzip image-bluejay-cp3a.261005.002.a1.zip 
Archive:  image-bluejay-cp3a.261005.002.a1.zip
  inflating: android-info.txt        
  inflating: fastboot-info.txt       
  inflating: product.img             
  inflating: dtbo.img                
  inflating: vendor.img              
  inflating: system_ext.img          
  inflating: system_other.img        
  inflating: system.img              
  inflating: boot.img                
  inflating: vbmeta_system.img       
  inflating: super_empty.img         
  inflating: vendor_dlkm.img         
  inflating: pvmfw.img               
  inflating: vbmeta_vendor.img       
  inflating: vendor_boot.img         
  inflating: vbmeta.img              
  inflating: abl.img                 
  inflating: bl1.img                 
  inflating: bl2.img                 
  inflating: bl31.img                
  inflating: gsa.img                 
  inflating: ldfw.img                
  inflating: modem.img               
  inflating: pbl.img                 
  inflating: tzsw.img
```

## Restore boot.img

```
$ adb reboot bootloader
$ fastboot flash boot boot.img
$ fastboot reboot
```

## KernelSU-Next

References:
- https://github.com/KernelSU-Next/KernelSU-Next/releases


### Install KernelSU-Next manager

```
$ wget https://github.com/KernelSU-Next/KernelSU-Next/releases/download/v3.4.2/KernelSU_Next_v3.4.2-spoofed_33355-release.apk
$ wget https://github.com/KernelSU-Next/KernelSU-Next/releases/download/v3.4.2/KernelSU_Next_v3.4.2_33355-release.apk
$ apkanalyzer manifest application-id KernelSU_Next_v3.4.2-spoofed_33355-release.apk 
kqvdie.zeykvw.hpbcyd
$ apkanalyzer manifest application-id KernelSU_Next_v3.4.2_33355-release.apk 
com.rifsxd.ksunext
$ adb install KernelSU_Next_v3.4.2-spoofed_33355-release.apk 
Performing Streamed Install
Success
```

### Patch boot.img

```
$ adb push boot.img /sdcard/Download/
```

KernelSU-Next manager --> Install --> Select a file --> boot.img

```
$ adb pull /sdcard/Download/kernelsu_next_patched_20261015_182231.img
```

### Flash boot.img

```
$ adb reboot bootloader
$ fastboot flash boot kernelsu_next_patched_20261015_182231.img
$ fastboot reboot
```

### Enable su

KernelSU-Next manager --> Superuser --> Shell --> enable

```
$ adb shell
bluejay:/ $ su
bluejay:/ #
```

## Magisk

References:
- https://github.com/topjohnwu/magisk

### Install Magisk

```
$ wget https://github.com/topjohnwu/Magisk/releases/download/v30.7/Magisk-v30.7.apk
$ adb install Magisk-v30.7.apk
```

### Patch boot.img

```
$ adb push boot.img /sdcard/Download/
```

Magisk --> Install --> Select and patch a file --> LET'S GO

```
$ adb pull /sdcard/Download/magisk_patched-30700_xpRGa.img
```

### Flash boot.img

```
$ adb reboot bootloader
$ fastboot flash boot magisk_patched-30700_xpRGa.img
$ fastboot reboot
```

### Enable su

```
$ adb shell
bluejay:/ $ su
bluejay:/ #
```

Magisk --> grant
