LLVM=/opt/llvm/bin
PLUGIN=$PWD/build/libLLVMObfuscator.so
SYSROOT=/opt/a64
T="--target=aarch64-linux-gnu --sysroot=$SYSROOT"

$LLVM/clang $T -O1 -S -emit-llvm test_sub.c -o test_sub_a64.ll
$LLVM/opt -load-pass-plugin "$PLUGIN" -passes='function(substitution)' -S test_sub_a64.ll -o test_sub_a64_obf.ll
$LLVM/llc --relocation-model=pic -filetype=obj test_sub_a64_obf.ll -o test_sub_a64_obf.o
$LLVM/clang $T -fuse-ld=lld test_sub_a64_obf.o -o test_sub_a64_obf

file test_sub_a64_obf
