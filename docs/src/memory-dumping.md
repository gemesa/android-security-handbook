# Memory dumping

## Use case

Capture the mapped memory of a process to recover values from RAM.

## Explanation

The list of mapped regions is available through `/proc/<pid>/maps`. The content of these regions can be read via `/proc/<pid>/mem`. It is a good idea to freeze the process first, then dump the memory. For now, we only dump `rw-p` regions.

There are other solutions available for dumping memory, e.g. [hexdump](https://frida.re/docs/javascript-api/#hexdump), [fridump](https://github.com/Nightbringer21/fridump) or [`gdb` and `lldb`](https://lldb.llvm.org/use/map.html#save-binary-memory-data-starting-at-0x1000-and-ending-at-0x2000-to-a-file). The main problem is that attaching to a process with `frida`, `gdb` and `lldb` can be detected.

## Usage

```
$ cargo build --release --target aarch64-linux-android
$ adb push target/aarch64-linux-android/release/dumpmem /data/local/tmp/
```

Phone:

```
# ps -ef | grep test                                                                                      
u0_a220       5542   465 0 22:02:57 ?     00:00:02 com.example.test
u0_a220       5984   465 1 22:53:24 ?     00:00:00 com.example.test:worker2
u0_a220       5985   465 1 22:53:24 ?     00:00:00 com.example.test:worker1
root          6093  5955 0 22:55:00 pts/1 00:00:00 grep test
# ./dumpmem -p com.example.test -p com.example.test:worker1                                               
Found PIDs: [5542, 5985]
Stopping PIDs: [5542, 5985]
Dumping rw-p regions...
Done: /data/local/tmp/memdump_5542
Dumping rw-p regions...
Done: /data/local/tmp/memdump_5985
Resuming PIDs: [5542, 5985]
# ls memdump_5542/bin | head -n 5                                                                         
2000000-e000000.bin
26000000-32000000.bin
4a000000-4a002000.bin
57e9108b0000-57e9108b1000.bin
6ffb4000-702a0000.bin
# head -n 5 memdump_5542/dumpmem.log                                                                      
02000000-0e000000 rw-p 00000000 00:00 0                                  [anon:dalvik-main space]
26000000-32000000 rw-p 00000000 00:00 0                                  [anon:dalvik-free list large object space]
4a000000-4a002000 rw-p 00000000 00:00 0 
4a002000-4c002000 r--s 00000000 00:01 1040                               /memfd:jit-zygote-cache (deleted)
4c002000-4e002000 r-xs 02000000 00:01 1040                               [anon_shmem:dalvik-zygote-jit-code-cache]
```

## Code

```rust
{{#include ../../src/dumpmem/src/main.rs}}
```

[View on GitHub](https://github.com/gemesa/android-security-handbook/blob/main/src/dumpmem/src/main.rs).
