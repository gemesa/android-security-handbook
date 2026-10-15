# Pixel 6a rooting guide

## Prerequisites

- enable the following in developer options:
   - OEM unlocking
   - USB debugging
- check: Settings --> ABout phone --> Build number: CP1A.260405.005
  - https://developers.google.com/android/images#bluejay
  - `wget https://dl.google.com/dl/android/aosp/bluejay-cp1a.260405.005-factory-1267628c.zip`

```
$ adb reboot bootloader
$ fastboot flashing unlock
```

```
$ unzip bluejay-cp1a.260405.005-factory-1267628c.zip           
Archive:  bluejay-cp1a.260405.005-factory-1267628c.zip
   creating: bluejay-cp1a.260405.005/
  inflating: bluejay-cp1a.260405.005/flash-all.bat  
 extracting: bluejay-cp1a.260405.005/image-bluejay-cp1a.260405.005.zip  
  inflating: bluejay-cp1a.260405.005/d3m2.ec.bin  
  inflating: bluejay-cp1a.260405.005/proto11.ec.bin  
  inflating: bluejay-cp1a.260405.005/bootloader-bluejay-bluejay-16.4-14548185.img  
  inflating: bluejay-cp1a.260405.005/evt.ec.bin  
  inflating: bluejay-cp1a.260405.005/flash-base.sh  
  inflating: bluejay-cp1a.260405.005/flash-all.sh  
  inflating: bluejay-cp1a.260405.005/radio-bluejay-g5123b-145971-260109-b-14688209.img
$ unzip bluejay-cp1a.260405.005/image-bluejay-cp1a.260405.005.zip
Archive:  bluejay-cp1a.260405.005/image-bluejay-cp1a.260405.005.zip
  inflating: android-info.txt        
  inflating: fastboot-info.txt       
 extracting: boot.img                
  inflating: dtbo.img                
  inflating: vendor_boot.img         
  inflating: system.img              
  inflating: vendor.img              
  inflating: product.img             
  inflating: system_ext.img          
  inflating: vendor_dlkm.img         
  inflating: system_other.img        
  inflating: pvmfw.img               
  inflating: vbmeta_system.img       
  inflating: vbmeta_vendor.img       
  inflating: vbmeta.img              
  inflating: super_empty.img         
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
