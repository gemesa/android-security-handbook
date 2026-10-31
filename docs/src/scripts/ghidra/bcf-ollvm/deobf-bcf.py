# Remove obfuscator-llvm bogus control flow (bcf) from listing and decompiler views.
# https://github.com/eshard/obfuscator-llvm/blob/main/bogus/BogusControlFlow.cpp
#
# predicates: (y < 10 || x * (x + 1) % 2 == 0), always true
# https://github.com/eshard/obfuscator-llvm/blob/ad26aa21b90cc5c5118d32114b674d1455f54168/bogus/BogusControlFlow.cpp#L43
#
# Ghidra cannot prove the "always true" part so we give it x, y concrete values:
# 0 (.bss) and let the decompiler constant fold.
#
# Step 1:
#   0 fill .bss and mark x, y as constants. The decompiler folds
#   the predicates and hides the bogus blocks.
#
# Step 2:
#   The decompiler lists the hidden blocks ("Removing unreachable block").
#   Any branch that can go to a hidden block is essentially a one way branch:
#     - target hidden -> never taken -> replace with nop
#     - fall-through hidden -> always taken -> replace with b target
#
# @category Deobfuscation

import re
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.app.decompiler import DecompileOptions
from ghidra.app.decompiler.flatapi import FlatDecompilerAPI
from ghidra.program.flatapi import FlatProgramAPI
from ghidra.app.plugin.assembler import Assemblers
from ghidra.program.model.data import MutabilitySettingsDefinition as Mutability

# x, y, x.1, y.2, ...
OPAQUE_NAME = re.compile(r"^[xy]([._]\d+)?$")
# /* WARNING: Removing unreachable block (ram,0x00110968) */
DEAD_BLOCK = re.compile(r"Removing unreachable block \(\w+,0x([0-9a-fA-F]+)\)")


# step 1


def find_opaque_globals():
    opaque = []
    for sym in currentProgram.getSymbolTable().getAllSymbols(True):
        if not OPAQUE_NAME.match(sym.getName()):
            continue  # not named x, y, x.1, y.2, ...
        if not sym.getAddress().isMemoryAddress():
            continue  # e.g. a local variable named x (stack/register, not a global)
        opaque.append(sym)
    return opaque


def mark_constant(sym):
    addr = sym.getAddress()

    # Ghidra models .bss as uninitialized and the decompiler will not
    # read a value from it. We 0 fill it like the loader does at runtime.
    block = getMemoryBlock(addr)
    if not block.isInitialized():
        currentProgram.getMemory().convertToInitialized(block, 0)

    # mark x/y constant (Ghidra defines them as undefined4)
    Mutability.DEF.setChoice(getDataAt(addr), Mutability.CONSTANT)
    print("%-4s @ %s" % (sym.getName(), addr))


# step 2


def dead_blocks(func):
    decomp = FlatDecompilerAPI(FlatProgramAPI(currentProgram, monitor))
    # Without an options object the decompiler might leave out the
    # "Removing unreachable block" warnings.
    decomp.initialize()
    opts = DecompileOptions()
    opts.grabFromProgram(currentProgram)
    # the warning comments are on by default (uncomment if they are missing)
    # opts.setHeadCommentIncluded(True)
    # opts.setWARNCommentIncluded(True)
    decomp.getDecompiler().setOptions(opts)

    try:
        c_code = decomp.decompile(func, 60)  # 60 s timeout
    finally:
        decomp.dispose()
    # /* WARNING: Removing unreachable block (ram,0x00110968) */
    dead = set()
    for hex_addr in DEAD_BLOCK.findall(c_code):
        dead.add(int(hex_addr, 16))  # "00110810" -> 0x110810
    return dead


def patch_branches(func, dead):
    asm = Assemblers.getAssembler(currentProgram)
    # collect conditional jumps (tbz, cbz, b.gt, ...)
    # skip plain b, bl, ret
    branches = []
    for insn in currentProgram.getListing().getInstructions(func.getBody(), True):
        flow = insn.getFlowType()
        if flow.isConditional() and flow.isJump():
            branches.append(insn)

    patched = 0
    for insn in branches:
        addr = insn.getAddress()
        target = insn.getFlows()[0].getOffset()  # jump target
        fall = insn.getFallThrough().getOffset()  # fallthrough target

        if fall in dead and target not in dead:
            # The fallthrough is never taken -> it always jumps.
            #   0x1107f8  ldr   w8,[x22]          ; w8 = x
            #   0x1107fc  adrp  x23,0x120000
            #   0x110800  ldr   x23,[x23,#->y]    ; x23 = &y
            #   0x110804  sub   w9,w8,#1          ; w9 = x - 1
            #   0x110808  mul   w8,w8,w9          ; w8 = x * (x - 1)
            #   0x11080c  tbz   w8,#0,0x11081c    ; bit 0 is 0 (even) -> always jumps
            #   0x110810  ldr   w8,[x23]          ; dead
            #   0x110814  cmp   w8,#9             ; dead
            #   0x110818  b.gt  0x1107f8          ; dead
            #   0x11081c  cmp   w21,#2            ; jump target
            # becomes
            #   0x11080c  b     0x11081c
            asm.assemble(addr, "b 0x%x" % target)
        elif target in dead and fall not in dead:
            # The jump is never taken -> it always falls through.
            #   0x11096c  cset  w8,lt             ; w8 = predicate = 1 (always)
            #   ...
            #   0x110998  cbz   w8,0x1109c8       ; w8 == 0? never -> never jumps
            #   0x11099c  mov   w0,w19            ; live
            #   0x1109a0  mov   w1,w21            ; live
            #   0x1109a4  bl    mix               ; live
            # becomes
            #   0x110998  nop
            asm.assemble(addr, "nop")
        else:
            # Both paths live.
            # Both paths dead.
            continue
        patched += 1

    # Recompute the function from its entry point. Dead blocks are dropped.
    CreateFunctionCmd.fixupFunctionBody(currentProgram, func, monitor)
    print("%s: patched %d opaque branch(es)" % (func.getName(), patched))


def main():
    opaque = find_opaque_globals()
    if not opaque:
        print("No x, y globals found.")
        return
    for sym in opaque:
        mark_constant(sym)

    func = getFunctionContaining(currentAddress)
    if func is None:
        print("Move the cursor in the target function.")
        return

    dead = dead_blocks(func)
    if not dead:
        print("%s: no unreachable blocks found" % func.getName())
        return

    patch_branches(func, dead)


main()
