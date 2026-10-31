# @category Deobfuscation

from ghidra.app.emulator import EmulatorHelper

"""
void _INIT_0(void)

{
  ulong uVar1;
  undefined1 local_8 [8];
  
  uVar1 = 0;
  do {
    (&DAT_001088c0)[uVar1] = *(byte *)((ulong)local_8 | uVar1 & 7) ^ (&DAT_001088c0)[uVar1];
    uVar1 = uVar1 + 1;
  } while (uVar1 != 0x2f);
  return;
}
"""

# fmt: off
ctors = [(0x0010062C, 0x001088C0, 0x2F)]
# fmt: on

for func, dst, size in ctors:
    emu = EmulatorHelper(currentProgram)
    # arbitrary addresses
    emu.writeRegister("sp", 0x2000000)
    emu.writeRegister("x30", 0x1000)
    emu.writeRegister("pc", func)
    emu.setBreakpoint(toAddr("0x1000"))
    emu.run(monitor)

    data = emu.readMemory(toAddr(hex(dst)), size - 1)
    text = "".join(chr(b & 0xFF) for b in data)
    print('%s: decrypted string: "%s"' % (hex(dst), text))
    emu.dispose()