#!/usr/bin/env bash
set -euo pipefail

LLVM=/opt/llvm/bin
PLUGIN=$PWD/../build/libLLVMObfuscator.so
SYSROOT=/opt/a64
T="--target=aarch64-linux-gnu --sysroot=$SYSROOT"

SRC=test_enc_str.c
OUT=test_enc_str_a64

$LLVM/clang $T -fuse-ld=lld -O1 $SRC -o ${OUT}
$LLVM/llvm-strip ${OUT}
