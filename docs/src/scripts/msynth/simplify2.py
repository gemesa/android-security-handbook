# https://github.com/cea-sec/miasm/blob/master/doc/expression/expression.ipynb

"""
...
  *(undefined8 *)(unaff_x19 + 0x840) = 0;
...
  (*(code *)((*(ulong *)(unaff_x19 + 0x840) ^ 0x32a6ad) +
            (*(ulong *)(unaff_x19 + 0x840) & 0x32a6ad) * 2))();
...
"""

"""
  (x ^ 0x32a6ad) + (x & 0x32a6ad) * 2
"""

from miasm.expression.expression import ExprId, ExprInt
from msynth import Synthesizer

k = lambda v: ExprInt(v, 64)

x = ExprId("x", 64)
e = (x ^ k(0x32a6ad)) + (x & k(0x32a6ad)) * k(2)
e.replace_expr({x: k(0)})
s = Synthesizer()

print(s.simplify(e))
