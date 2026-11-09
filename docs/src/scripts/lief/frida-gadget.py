import lief
lib = lief.parse("libnative-lib.so")
lib.add_library("libgadget.so.so")
lib.write("libnative-lib.so")
