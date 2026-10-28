# @category Deobfuscation

from ghidra.app.emulator import EmulatorHelper

"""
undefined8 FUN_001108b8(void)

{
  FUN_00110868(&DAT_00130be9,&DAT_001005d4);
  FUN_00110890(&DAT_00130bf0,&DAT_001005da);
  puts(&DAT_00130be9);
  puts(&DAT_00130bf0);
  return 0;
}
"""

# fmt: off
calls = [(0x00110868, 0x00130BE9, 0x001005D4),
         (0x00110890, 0x00130BF0, 0x001005DA)]
# fmt: on

for func, dst, src in calls:
    emu = EmulatorHelper(currentProgram)
    emu.writeRegister("x0", dst)
    emu.writeRegister("x1", src)
    # arbitrary address
    emu.writeRegister("x30", 0x1000)
    # arbitrary address
    emu.writeRegister("sp", 0x70000000)
    emu.writeRegister("pc", func)
    emu.setBreakpoint(toAddr("0x1000"))
    emu.run(monitor)

    data = emu.readMemory(toAddr(hex(dst)), 6)
    text = "".join(chr(b & 0xFF) for b in data)
    print('%s: decrypted string: "%s"' % (hex(dst), text))
    emu.dispose()
