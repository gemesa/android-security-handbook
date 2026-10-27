# obfuscator-llvm

## Use case

Obfuscate native code with LLVM IR level obfuscation passes.

## Explanation

[Maintained version](https://github.com/eshard/obfuscator-llvm) of the original [obfuscator-llvm](https://github.com/obfuscator-llvm/obfuscator).

Supported obfuscation passes:

- [CFG flattening](https://github.com/eshard/obfuscator-llvm/blob/main/flattening/Flattening.cpp)
- [Basic block splitting](https://github.com/eshard/obfuscator-llvm/blob/main/split/SplitBasicBlocks.cpp)
- [String encryption](https://github.com/eshard/obfuscator-llvm/blob/main/string/StringObfuscation.cpp)
- [Instruction substitution](https://github.com/eshard/obfuscator-llvm/blob/main/substitution/Substitution.cpp)

## Usage

General:

```
$ git clone git@github.com:llvm/llvm-project.git llvm-project-21
$ git switch release/21.x
$ cmake -S llvm -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DLLVM_PARALLEL_LINK_JOBS=1 -DLLVM_ENABLE_PROJECTS="clang" -DCMAKE_INSTALL_PREFIX=/opt/llvm
$ ninja -C build -j 12
$ sudo ninja install
```

```
$ sudo dnf install xxd
$ git clone https://github.com/eshard/obfuscator-llvm.git
$ cd obfuscator-llvm
$ mkdir -p build && cd build
$ cmake -G "Ninja" -DLLVM_DIR=/opt/llvm/lib/cmake ..
$ ninja -j$(nproc)
```

```
$ sudo dnf install qemu-user-static-aarch64
$ sudo dnf -y --forcearch=aarch64 --installroot=/opt/a64 --releasever=$(rpm -E %fedora) --use-host-config install glibc-devel gcc
$ sudo dnf install lld
```

```sh
LLVM=/opt/llvm/bin
PLUGIN=$PWD/build/libLLVMObfuscator.so
SYSROOT=/opt/a64
T="--target=aarch64-linux-gnu --sysroot=$SYSROOT"

$LLVM/clang $T -O1 -S -emit-llvm test_sub.c -o test_sub_a64.ll
$LLVM/opt -load-pass-plugin "$PLUGIN" -passes='function(substitution)' -S test_sub_a64.ll -o test_sub_a64_obf.ll
$LLVM/llc --relocation-model=pic -filetype=obj test_sub_a64_obf.ll -o test_sub_a64_obf.o
$LLVM/clang $T -fuse-ld=lld test_sub_a64_obf.o -o test_sub_a64_obf

file test_sub_a64_obf
```

```c
$ cat test_sub.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  int a = argc > 1 ? atoi(argv[1]) : 7;
  int b = argc > 2 ? atoi(argv[2]) : 3;
  printf("or=%d", a | b);
  return 0;
}
```

```
$ cat test_sub_a64.ll
; ModuleID = 'test_sub.c'
source_filename = "test_sub.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i8:8:32-i16:16:32-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "aarch64-unknown-linux-gnu"

@.str = private unnamed_addr constant [6 x i8] c"or=%d\00", align 1

; Function Attrs: nofree nounwind uwtable
define dso_local noundef i32 @main(i32 noundef %0, ptr nofree noundef readonly captures(none) %1) local_unnamed_addr #0 {
  %3 = icmp sgt i32 %0, 1
  br i1 %3, label %4, label %9

4:                                                ; preds = %2
  %5 = getelementptr inbounds nuw i8, ptr %1, i64 8
  %6 = load ptr, ptr %5, align 8, !tbaa !16
  %7 = tail call i64 @strtol(ptr noundef nonnull captures(none) %6, ptr noundef null, i32 noundef 10) #3, !inline_history !19
  %8 = trunc i64 %7 to i32
  br label %9

9:                                                ; preds = %2, %4
  %10 = phi i32 [ %8, %4 ], [ 7, %2 ]
  %11 = icmp sgt i32 %0, 2
  br i1 %11, label %12, label %17

12:                                               ; preds = %9
  %13 = getelementptr inbounds nuw i8, ptr %1, i64 16
  %14 = load ptr, ptr %13, align 8, !tbaa !16
  %15 = tail call i64 @strtol(ptr noundef nonnull captures(none) %14, ptr noundef null, i32 noundef 10) #3, !inline_history !19
  %16 = trunc i64 %15 to i32
  br label %17

17:                                               ; preds = %9, %12
  %18 = phi i32 [ %16, %12 ], [ 3, %9 ]
  %19 = or i32 %18, %10
  %20 = tail call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str, i32 noundef %19)
  ret i32 0
}

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr noundef readonly captures(none), ...) local_unnamed_addr #1

; Function Attrs: mustprogress nocallback nofree nounwind willreturn
declare i64 @strtol(ptr noundef readonly, ptr noundef captures(none), i32 noundef) local_unnamed_addr #2

attributes #0 = { nofree nounwind uwtable "frame-pointer"="non-leaf-no-reserve" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="generic" "target-features"="+fp-armv8,+neon,+outline-atomics,+v8a,-fmv" }
attributes #1 = { nofree nounwind "frame-pointer"="non-leaf-no-reserve" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="generic" "target-features"="+fp-armv8,+neon,+outline-atomics,+v8a,-fmv" }
attributes #2 = { mustprogress nocallback nofree nounwind willreturn "frame-pointer"="non-leaf-no-reserve" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="generic" "target-features"="+fp-armv8,+neon,+outline-atomics,+v8a,-fmv" }
attributes #3 = { nounwind }

!llvm.module.flags = !{!0, !1, !2, !3, !4, !5, !6, !7, !8, !9}
!llvm.ident = !{!10}
!llvm.errno.tbaa = !{!11}

!0 = !{i32 1, !"ptrauth-elf-got", i32 0}
!1 = !{i32 1, !"ptrauth-init-fini", i32 0}
!2 = !{i32 1, !"ptrauth-init-fini-address-discrimination", i32 0}
!3 = !{i32 1, !"ptrauth-sign-personality", i32 0}
!4 = !{i32 1, !"aarch64-elf-pauthabi-platform", i32 268435458}
!5 = !{i32 1, !"aarch64-elf-pauthabi-version", i32 0}
!6 = !{i32 8, !"PIC Level", i32 2}
!7 = !{i32 7, !"PIE Level", i32 2}
!8 = !{i32 7, !"uwtable", i32 2}
!9 = !{i32 7, !"frame-pointer", i32 4}
!10 = !{!"clang version 24.0.0git (https://github.com/llvm/llvm-project.git 56ed7f824a62ec3261ecdf57c51627dc7d58591c)"}
!11 = !{!12, !13, i64 0}
!12 = !{!"__libc_errno", !13, i64 0}
!13 = !{!"int", !14, i64 0}
!14 = !{!"omnipotent char", !15, i64 0}
!15 = !{!"Simple C/C++ TBAA"}
!16 = !{!17, !17, i64 0}
!17 = !{!"p1 omnipotent char", !18, i64 0}
!18 = !{!"any pointer", !14, i64 0}
!19 = distinct !{null}
```

```c
undefined8 main(int param_1,long param_2)

{
  uint uVar1;
  uint uVar2;
  long lVar3;
  
  if (param_1 < 2) {
    uVar1 = 7;
  }
  else {
    lVar3 = strtol(*(char **)(param_2 + 8),(char **)0x0,10);
    uVar1 = (uint)lVar3;
  }
  if (param_1 < 3) {
    uVar2 = 3;
  }
  else {
    lVar3 = strtol(*(char **)(param_2 + 0x10),(char **)0x0,10);
    uVar2 = (uint)lVar3;
  }
  printf("or=%d",((uVar2 ^ 0xffffffff) & 0xef27f53c | uVar2 & 0x10d80ac3) ^
                 ((uVar1 ^ 0xffffffff) & 0xef27f53c | uVar1 & 0x10d80ac3) |
                 (~uVar2 | uVar1 ^ 0xffffffff) ^ 0xffffffff);
  return 0;
}
```

```
$ cat test_sub_a64_obf.ll
; ModuleID = 'test_sub_a64.ll'
source_filename = "test_sub.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i8:8:32-i16:16:32-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "aarch64-unknown-linux-gnu"

@.str = private unnamed_addr constant [6 x i8] c"or=%d\00", align 1

; Function Attrs: nofree nounwind uwtable
define dso_local noundef i32 @main(i32 noundef %0, ptr nofree noundef readonly captures(none) %1) local_unnamed_addr #0 {
  %3 = icmp sgt i32 %0, 1
  br i1 %3, label %4, label %9

4:                                                ; preds = %2
  %5 = getelementptr inbounds nuw i8, ptr %1, i64 8
  %6 = load ptr, ptr %5, align 8, !tbaa !16
  %7 = tail call i64 @strtol(ptr noundef nonnull captures(none) %6, ptr noundef null, i32 noundef 10) #3, !inline_history !19
  %8 = trunc i64 %7 to i32
  br label %9

9:                                                ; preds = %4, %2
  %10 = phi i32 [ %8, %4 ], [ 7, %2 ]
  %11 = icmp sgt i32 %0, 2
  br i1 %11, label %12, label %17

12:                                               ; preds = %9
  %13 = getelementptr inbounds nuw i8, ptr %1, i64 16
  %14 = load ptr, ptr %13, align 8, !tbaa !16
  %15 = tail call i64 @strtol(ptr noundef nonnull captures(none) %14, ptr noundef null, i32 noundef 10) #3, !inline_history !19
  %16 = trunc i64 %15 to i32
  br label %17

17:                                               ; preds = %12, %9
  %18 = phi i32 [ %16, %12 ], [ 3, %9 ]
  %19 = xor i32 %18, -1
  %20 = xor i32 %10, -1
  %21 = xor i32 -282593988, -1
  %22 = and i32 %19, -282593988
  %23 = and i32 %18, %21
  %24 = and i32 %20, -282593988
  %25 = and i32 %10, %21
  %26 = or i32 %22, %23
  %27 = or i32 %24, %25
  %28 = xor i32 %26, %27
  %29 = or i32 %19, %20
  %30 = xor i32 %29, -1
  %31 = or i32 -282593988, %21
  %32 = and i32 %30, %31
  %33 = or i32 %28, %32
  %34 = or i32 %18, %10
  %35 = tail call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str, i32 noundef %33)
  ret i32 0
}

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr noundef readonly captures(none), ...) local_unnamed_addr #1

; Function Attrs: mustprogress nocallback nofree nounwind willreturn
declare i64 @strtol(ptr noundef readonly, ptr noundef captures(none), i32 noundef) local_unnamed_addr #2

attributes #0 = { nofree nounwind uwtable "frame-pointer"="non-leaf-no-reserve" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="generic" "target-features"="+fp-armv8,+neon,+outline-atomics,+v8a,-fmv" }
attributes #1 = { nofree nounwind "frame-pointer"="non-leaf-no-reserve" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="generic" "target-features"="+fp-armv8,+neon,+outline-atomics,+v8a,-fmv" }
attributes #2 = { mustprogress nocallback nofree nounwind willreturn "frame-pointer"="non-leaf-no-reserve" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="generic" "target-features"="+fp-armv8,+neon,+outline-atomics,+v8a,-fmv" }
attributes #3 = { nounwind }

!llvm.module.flags = !{!0, !1, !2, !3, !4, !5, !6, !7, !8, !9}
!llvm.ident = !{!10}
!llvm.errno.tbaa = !{!11}

!0 = !{i32 1, !"ptrauth-elf-got", i32 0}
!1 = !{i32 1, !"ptrauth-init-fini", i32 0}
!2 = !{i32 1, !"ptrauth-init-fini-address-discrimination", i32 0}
!3 = !{i32 1, !"ptrauth-sign-personality", i32 0}
!4 = !{i32 1, !"aarch64-elf-pauthabi-platform", i32 268435458}
!5 = !{i32 1, !"aarch64-elf-pauthabi-version", i32 0}
!6 = !{i32 8, !"PIC Level", i32 2}
!7 = !{i32 7, !"PIE Level", i32 2}
!8 = !{i32 7, !"uwtable", i32 2}
!9 = !{i32 7, !"frame-pointer", i32 4}
!10 = !{!"clang version 24.0.0git (https://github.com/llvm/llvm-project.git 56ed7f824a62ec3261ecdf57c51627dc7d58591c)"}
!11 = !{!12, !13, i64 0}
!12 = !{!"__libc_errno", !13, i64 0}
!13 = !{!"int", !14, i64 0}
!14 = !{!"omnipotent char", !15, i64 0}
!15 = !{!"Simple C/C++ TBAA"}
!16 = !{!17, !17, i64 0}
!17 = !{!"p1 omnipotent char", !18, i64 0}
!18 = !{!"any pointer", !14, i64 0}
!19 = distinct !{null}
```

Android:

See [ANDROID_NDK.md](https://github.com/eshard/obfuscator-llvm/blob/main/docs/ANDROID_NDK.md).

References:
- https://github.com/eshard/obfuscator-llvm
- https://github.com/za233/Polaris-Obfuscator/tree/main
- https://github.com/Apich-Organization/ensia
