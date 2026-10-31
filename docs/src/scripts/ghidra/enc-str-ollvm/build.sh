#!/usr/bin/env bash
set -euo pipefail

LLVM=/opt/llvm/bin
PLUGIN=$HOME/git-repos/obfuscator-llvm/build/libLLVMObfuscator.so
SYSROOT=/opt/a64
T="--target=aarch64-linux-gnu --sysroot=$SYSROOT"

SRC=test_enc_str.c
OUT=test_enc_str_a64

$LLVM/clang $T -O1 -fPIC -S -emit-llvm $SRC -o ${OUT}.ll
$LLVM/llc -filetype=obj ${OUT}.ll -o ${OUT}.o
$LLVM/clang $T -fuse-ld=lld ${OUT}.o -o ${OUT}

$LLVM/opt -load "$PLUGIN" -load-pass-plugin "$PLUGIN" \
	-passes='string-encryption' -S ${OUT}.ll -o ${OUT}_obf.ll

$LLVM/llc -filetype=obj ${OUT}_obf.ll -o ${OUT}_obf.o
$LLVM/clang $T -fuse-ld=lld ${OUT}_obf.o -o ${OUT}_obf

$LLVM/clang $T -shared -fuse-ld=lld ${OUT}_obf.o -o lib${OUT}_obf.so
