from miasm.expression.expression import ExprId, ExprInt
from miasm.expression.simplifications import expr_simp

x = ExprId("x", 32)
k = lambda v: ExprInt(v, 32)

e = (x << k(3)) + (x << k(2)) + (x << k(1))

print("Original:  ", e)
print("Simplified:", expr_simp(e))
