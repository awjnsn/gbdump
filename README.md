# gbdump
## A not so fully featured disassembler for the Nintendo&reg; Gameboy
### Overview

gbdump is a disassembler, written in Python 3, for Nintendo&reg; Gameboy games.  It features built in hashing, header analysis, and basic linear disassembly in pseudo-[RGBDS](https://github.com/rednex/rgbds) syntax.  It was created as a project for CS-4984 Software Reverse Engineering at Virginia Tech.

### Usage

`./gbdump.py rom_file output_file`

### Known Issues

Disassembly is strictly linear, with the only exception being that the header section is automatically skipped.  As a result, data is interpreted as instructions, leading to inaccurate disassembly and misaligned instructions. 

### Useful Resources

[Gameboy Pan Docs](http://bgb.bircd.org/pandocs.htm)

[Gameboy CPU Opcode Table](http://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html)
