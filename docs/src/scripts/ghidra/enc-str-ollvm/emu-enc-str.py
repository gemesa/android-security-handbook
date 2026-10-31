# @category Deobfuscation

from ghidra.app.emulator import EmulatorHelper

"""
void tcyrHvkBDbRhVVf(void)

{
  YTKkx8dqnaDxN8a(&str1,7,0x5a);
  YTKkx8dqnaDxN8a(&str2,7,0x16);
  return;
}
"""

# fmt: off
calls = [(0x00110774, 0x00130A20, 7, 0x5A),
         (0x00110774, 0x00130A27, 7, 0x16)]
# fmt: on

for func, dst, size, key in calls:
    emu = EmulatorHelper(currentProgram)
    emu.writeRegister("x0", dst)
    emu.writeRegister("x1", size)
    emu.writeRegister("x2", key)
    # arbitrary address
    emu.writeRegister("x30", 0x1000)
    emu.writeRegister("pc", func)
    emu.setBreakpoint(toAddr("0x1000"))
    emu.run(monitor)

    data = emu.readMemory(toAddr(hex(dst)), size - 1)
    text = "".join(chr(b & 0xFF) for b in data)
    print('%s: decrypted string: "%s"' % (hex(dst), text))
    emu.dispose()
