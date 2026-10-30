#!/usr/bin/env bash
set -euo pipefail

LLVM=/opt/llvm/bin
PLUGIN=$PWD/../build/libLLVMObfuscator.so
SYSROOT=/opt/a64
T="--target=aarch64-linux-gnu --sysroot=$SYSROOT"

SRC=test_bcf.c
OUT=test_bcf_a64

export LLVM_OBF_SEED=0xA04252B187478C00A40BC6D81D1A8A52

$LLVM/clang $T -O1 -S -emit-llvm $SRC -o ${OUT}.ll
$LLVM/llc --relocation-model=pic -filetype=obj ${OUT}.ll -o ${OUT}.o
$LLVM/clang $T -fuse-ld=lld ${OUT}.o -o ${OUT}

$LLVM/opt -load "$PLUGIN" -load-pass-plugin "$PLUGIN" \
	-bcf_prob=100 -bcf_loop=1 \
	-passes='function(bogus)' -S ${OUT}.ll -o ${OUT}_obf.ll

$LLVM/llc --relocation-model=pic -filetype=obj ${OUT}_obf.ll -o ${OUT}_obf.o
$LLVM/clang $T -fuse-ld=lld ${OUT}_obf.o -o ${OUT}_obf

echo "opaque globals in IR:"
grep -E '^@(x|y)(\.[0-9]+)? ' ${OUT}_obf.ll || true

$LLVM/clang $T -shared -fuse-ld=lld ${OUT}_obf.o -o lib${OUT}_obf.so
