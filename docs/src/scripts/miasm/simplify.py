from miasm.expression.expression import ExprId, ExprInt
from miasm.expression.simplifications import expr_simp

x = ExprId("x", 64)
k = lambda v: ExprInt(v, 64)

e = (x ^ k(0x32a86d)) + ((x & k(0x32a86d)) * k(2))
e = e.replace_expr({x: k(0)})

print(expr_simp(e))
