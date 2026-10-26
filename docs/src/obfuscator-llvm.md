# obfuscator-llvm

## Use case

Obfuscate native code with LLVM IR level obfuscation passes.

## Explanation

Maintained version of the original [obfuscator-llvm](https://github.com/obfuscator-llvm/obfuscator).

Supported obfuscation passes:

- CFG flattening
- Basic block splitting
- String encryption
- Instruction substitution

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

```
$ cat test_sub_a64.ll 
; ModuleID = 'test_sub.c'
source_filename = "test_sub.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i8:8:32-i16:16:32-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "aarch64-unknown-linux-gnu"

@.str = private unnamed_addr constant [35 x i8] c"add=%d sub=%d and=%d or=%d xor=%d\0A\00", align 1

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
  %19 = add nsw i32 %18, %10
  %20 = sub nsw i32 %10, %18
  %21 = and i32 %18, %10
  %22 = or i32 %18, %10
  %23 = xor i32 %18, %10
  %24 = tail call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str, i32 noundef %19, i32 noundef %20, i32 noundef %21, i32 noundef %22, i32 noundef %23)
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

```
$ cat test_sub_a64_obf.ll
; ModuleID = 'test_sub_a64.ll'
source_filename = "test_sub.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i8:8:32-i16:16:32-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "aarch64-unknown-linux-gnu"

@.str = private unnamed_addr constant [35 x i8] c"add=%d sub=%d and=%d or=%d xor=%d\0A\00", align 1

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
  %19 = sub i32 0, %18
  %20 = sub i32 0, %10
  %21 = add i32 %19, %20
  %22 = sub i32 0, %21
  %23 = add nsw i32 %18, %10
  %24 = sub i32 0, %18
  %25 = add i32 %10, %24
  %26 = sub nsw i32 %10, %18
  %27 = xor i32 %10, -1
  %28 = xor i32 %18, %27
  %29 = and i32 %28, %18
  %30 = and i32 %18, %10
  %31 = xor i32 %18, -1
  %32 = xor i32 %10, -1
  %33 = xor i32 385505941, -1
  %34 = and i32 %31, 385505941
  %35 = and i32 %18, %33
  %36 = and i32 %32, 385505941
  %37 = and i32 %10, %33
  %38 = or i32 %34, %35
  %39 = or i32 %36, %37
  %40 = xor i32 %38, %39
  %41 = or i32 %31, %32
  %42 = xor i32 %41, -1
  %43 = or i32 385505941, %33
  %44 = and i32 %42, %43
  %45 = or i32 %40, %44
  %46 = or i32 %18, %10
  %47 = xor i32 %18, -1
  %48 = and i32 473511061, %47
  %49 = xor i32 473511061, -1
  %50 = and i32 %18, %49
  %51 = xor i32 %10, -1
  %52 = and i32 %51, 473511061
  %53 = and i32 %10, %49
  %54 = or i32 %48, %50
  %55 = or i32 %52, %53
  %56 = xor i32 %54, %55
  %57 = xor i32 %18, %10
  %58 = tail call i32 (ptr, ...) @printf(ptr noundef nonnull dereferenceable(1) @.str, i32 noundef %22, i32 noundef %25, i32 noundef %29, i32 noundef %45, i32 noundef %56)
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
