# bpftrace

## Use case

Trace [syscalls](https://man7.org/linux/man-pages/man2/syscalls.2.html) via [eBPF](https://ebpf.io/what-is-ebpf/).

## Explanation

See [bpftrace](https://github.com/bpftrace/bpftrace/tree/master) and [bpftrace docs](https://bpftrace.org/).

## Usage

```
$ wget https://github.com/bpftrace/bpftrace/releases/download/v0.27.1/bpftrace-aarch64
$ chmod +x bpftrace-aarch64
$ adb push bpftrace-aarch64 /data/local/tmp/
```

Check what events are available:

```
$ adb shell
bluejay:/ $ su
bluejay:/ # cd /data/local/tmp
bluejay:/data/local/tmp # zcat /proc/config.gz | grep -E 'FTRACE_SYSCALLS|HAVE_SYSCALL_TRACEPOINTS'
CONFIG_HAVE_SYSCALL_TRACEPOINTS=y
# CONFIG_FTRACE_SYSCALLS is not set
```

`CONFIG_FTRACE_SYSCALLS` is not set so we do not have per-syscall (`syscalls:*`) events:

```
bluejay:/data/local/tmp # ./bpftrace-aarch64 -l 'tracepoint:syscalls:*' | head
./bpftrace-aarch64: stat /bugreports: No such file or directory
./bpftrace-aarch64: stat /adb_keys: No such file or directory
WARNING: Could not read functions from /sys/kernel/tracing/available_filter_functions. If this is expected, use --traceable-functions to set this path manually. This file is needed in order to determine which functions can safely be traced without causing issues in the kernel.
```

Only raw syscalls:

```
bluejay:/data/local/tmp # ./bpftrace-aarch64 -l 'tracepoint:raw_syscalls:*' | head
./bpftrace-aarch64: stat /bugreports: No such file or directory
./bpftrace-aarch64: stat /adb_keys: No such file or directory
WARNING: Could not read functions from /sys/kernel/tracing/available_filter_functions. If this is expected, use --traceable-functions to set this path manually. This file is needed in order to determine which functions can safely be traced without causing issues in the kernel.
tracepoint:raw_syscalls:sys_enter
tracepoint:raw_syscalls:sys_exit
```

Trace [`reboot`](https://github.com/torvalds/linux/blob/d48723711bae9b8cdc56719c448ba42fef28cbee/scripts/syscall.tbl#L179) ([args](https://github.com/torvalds/linux/blob/d48723711bae9b8cdc56719c448ba42fef28cbee/include/linux/syscalls.h#L696)):

```
$ cat reboot.bt 
tracepoint:raw_syscalls:sys_enter /args.id == 142/ {
  printf("%s uid=%d magic1=0x%x magic2=0x%x cmd=0x%x arg=0x%lx\n",
         comm, uid, (uint32)args.args[0], (uint32)args.args[1],
         (uint32)args.args[2], args.args[3]);
}
```

```
$ apkanalyzer manifest application-id KernelSU_Next_v3.4.2-spoofed_33355-release.apk 
kqvdie.zeykvw.hpbcyd
```

```
bluejay:/data/local/tmp # dumpsys package kqvdie.zeykvw.hpbcyd | grep appId                                                                                                                         
    appId=10297
bluejay:/data/local/tmp # ./bpftrace-aarch64 reboot.bt
./bpftrace-aarch64: stat /bugreports: No such file or directory
./bpftrace-aarch64: stat /adb_keys: No such file or directory
WARNING: Could not read functions from /sys/kernel/tracing/available_filter_functions. If this is expected, use --traceable-functions to set this path manually. This file is needed in order to determine which functions can safely be traced without causing issues in the kernel.
Attached 1 probe
libksud.so uid=10297 magic1=0xdeadbeef magic2=0xcafebabe cmd=0x0 arg=0x7fdf0d6d4c
libksud.so uid=10297 magic1=0xdeadbeef magic2=0xcafebabe cmd=0x0 arg=0x7fdcdce99c
libksud.so uid=0 magic1=0xdeadbeef magic2=0xfafafafa cmd=0x555e2 arg=0x7fe1a4ea84
```

KernelSU-Next source references:
- <https://github.com/KernelSU-Next/KernelSU-Next/blob/eed26da24665bfe68ff9f7858fa6cfeea84fa345/uapi/supercall.h#L17>
- <https://github.com/KernelSU-Next/KernelSU-Next/blob/eed26da24665bfe68ff9f7858fa6cfeea84fa345/kernel/preinit/runner/runner.c#L340>
- <https://github.com/KernelSU-Next/KernelSU-Next/blob/eed26da24665bfe68ff9f7858fa6cfeea84fa345/userspace/ksud/src/susfsd.rs#L8>
- <https://github.com/KernelSU-Next/KernelSU-Next/blob/eed26da24665bfe68ff9f7858fa6cfeea84fa345/userspace/ksud/src/susfsd.rs#L231>

References:
- <https://github.com/bpftrace/bpftrace/blob/master/docs/tutorial_one_liners.md>
- <https://github.com/torvalds/linux/blob/master/scripts/syscall.tbl>
- <https://github.com/torvalds/linux/blob/master/include/linux/syscalls.h>
