from miasm.expression.expression import ExprId, ExprInt
from msynth import Synthesizer

uVar1 = ExprId("uVar1", 32)
uVar2 = ExprId("uVar2", 32)
k = lambda v: ExprInt(v, 32)

e = ((uVar2 ^ k(0xffffffff)) & k(0xef27f53c) | uVar2 & k(0x10d80ac3)) ^ \
    ((uVar1 ^ k(0xffffffff)) & k(0xef27f53c) | uVar1 & k(0x10d80ac3)) | \
    (~uVar2 | uVar1 ^ k(0xffffffff)) ^ k(0xffffffff)

s = Synthesizer()
left, right = e.args
print(s.simplify(s.simplify(left) | s.simplify(right)))
