import lief
lib = lief.parse("libnative-lib.so")
for s in lib.exported_functions:
    if s.name.startswith("Java_") or s.name == "JNI_OnLoad":
        print(hex(s.address), s.name)
