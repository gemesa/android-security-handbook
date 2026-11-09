import lief
lib = lief.parse("libnative-lib.so")
print("PIE:", lib.is_pie)
print("NX:", lib.has_nx)
print("Canary:", any(f.name == "__stack_chk_fail" for f in lib.imported_functions))
