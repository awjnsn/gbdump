from enum import Enum
from hashlib import md5

#Class to represent a Gameboy ROM
class ROM:

    #Initializes the ROM object
    def __init__(self, bytes):
        self.data = [int(b) for b in bytes]
        self.header = {
            "good_header" : self._check_header(),
            "title" : self._check_title(),
            "manufacturer_code" : self._check_mfg_code(),
            "cgb_flag" : self._check_cgb_flag(),
            "new_licensee_code" : self._check_new_licensee_code(),
            "sgb_flag" : self._check_sgb_flag(),
            "cartridge_type" : self._check_cart_type(),
            "rom_size" : self._check_rom_size(),
            "ram_size" : self._check_ram_size(),
            "destintation_code" : self._check_dest_code(),
            "old_licensee_code" : self._check_old_licensee_code(),
            "mask_rom_version_number" : self._check_mask_rom_ver_num(),
            "good_header_checksum" : self._check_header_checksum(),
            "good_global_checksum" : self._check_global_checksum()
        }

    #Enums
    class Cart_Type(Enum):
        ROM_ONLY = 0x00
        MBC1 = 0x01
        MBC1_PLUS_RAM = 0x02
        MBC1_PLUS_RAM_PLUS_BATTERY = 0x03
        MBC2 = 0x05
        MBC2_PLUS_BATTERY = 0x06
        ROM_PLUS_RAM = 0x08
        ROM_PLUS_RAM_PLUS_BATTERY = 0x09
        MMM01 = 0x0B
        MMM01_PLUS_RAM = 0x0C
        MMM01_PLUS_RAM_PLUS_BATTERY = 0x0D
        MBC3_PLUS_TIMER_PLUS_BATTERY = 0x0F
        MBC3_PLUS_TIMER_PLUS_RAM_PLUS_BATTERY = 0x10
        MBC3 = 0x11
        MBC3_PLUS_RAM = 0x12
        MBC3_PLUS_RAM_PLUS_BATTERY = 0x13
        MBC4 = 0x15
        MBC4_PLUS_RAM = 0x16
        MBC4_PLUS_RAM_PLUS_BATTERY = 0x17
        MBC5 = 0x19
        MBC5_PLUS_RAM = 0x1A
        MBC5_PLUS_RAM_PLUS_BATTERY = 0x1B
        MBC5_PLUS_RUMBLE = 0x1C
        MBC5_PLUS_RUMBLE_PLUS_RAM = 0x1D
        MBC5_PLUS_RUMBLE_PLUS_RAM_PLUS_BATTERY = 0x1E
        POCKET_CAMERA = 0xFC
        BANDAI_TAMA5 = 0xFD
        HuC3 = 0xFE
        HuC1_PLUS_RAM_PLUS_BATTERY = 0xFF

    class ROM_Size(Enum):
        S_32_KByte = 0x00
        S_64_KByte = 0x01
        S_128_KByte = 0x02
        S_256_KByte = 0x03
        S_512_KByte = 0x04
        S_1_MByte = 0x05
        S_2_MByte = 0x06
        S_4_MByte = 0x07
        S_1_1_MByte = 0x52
        S_1_2_MByte = 0x53
        S_1_5_MByte = 0x54

    class RAM_Size(Enum):
        S_None = 0x00
        S_2_KByte = 0x01
        S_8_KByte = 0x02
        S_32_KByte = 0x03

    class Dest_Code(Enum):
        JAPAN = 0x00
        NON_JAPANESE = 0x01

    #Helper functions

    #Converts a range in the ROM to an ascii string
    def _range_to_str(self, start, end):
        data_range = [chr(c) for c in self.data[start:end]]
        return "".join(list(filter(lambda x: x != '\x00', data_range)))

    #Match a value to its associated enum
    def _match_enum(self, needle, haystack):
        for e in haystack:
            if needle == e.value:
                return e

    #Header data retrieval functions 

    #Checks to see if the ROM contains the Nintendo Logo
    def _check_header(self):
        return self.data[0x104:0x134] == [
            0xCE, 0xED, 0x66, 0x66, 0xCC, 0x0D, 0x00, 0x0B,
            0x03, 0x73, 0x00, 0x83, 0x00, 0x0C, 0x00, 0x0D,
            0x00, 0x08, 0x11, 0x1F, 0x88, 0x89, 0x00, 0x0E,
            0xDC, 0xCC, 0x6E, 0xE6, 0xDD, 0xDD, 0xD9, 0x99,
            0xBB, 0xBB, 0x67, 0x63, 0x6E, 0x0E, 0xEC, 0xCC,
            0xDD, 0xDC, 0x99, 0x9F, 0xBB, 0xB9, 0x33, 0x3E
        ]

    #Returns the title as a string
    def _check_title(self):
        #Note that the pandocs say 0x134 to 0x143
        return self._range_to_str(0x134, 0x142)

    #Returns the mfg code as a string
    def _check_mfg_code(self):
        mfg_str = self._range_to_str(0x13F, 0x142)
        return "No Code" if len(mfg_str) == 0 else mfg_str

    #Returns the cgb flag
    def _check_cgb_flag(self):
        return self.data[0x143]

    #Returns the new licensee code as a string
    def _check_new_licensee_code(self):
        licensee_code_str = self._range_to_str(0x144, 0x145)
        return "No Code" if len(licensee_code_str) == 0 else licensee_code_str

    #Returns the sgb flag
    def _check_sgb_flag(self):
        return self.data[0x146]

    #Returns an enum representing the cartridge type
    def _check_cart_type(self):
        return self._match_enum(self.data[0x147], self.Cart_Type)

    #Returns an enum representing the ROM size
    def _check_rom_size(self):
        return self._match_enum(self.data[0x148], self.ROM_Size)

    #Returns an enum representing the RAM size
    def _check_ram_size(self):
        return self._match_enum(self.data[0x149], self.RAM_Size)

    #Returns an enum representing the destination code
    def _check_dest_code(self):
        return self._match_enum(self.data[0x14A], self.Dest_Code)

    #Returns the old licensee code
    def _check_old_licensee_code(self):
        return self.data[0x14B]

    #Returns the mask rom version number
    def _check_mask_rom_ver_num(self):
        return self.data[0x14C]

    #Returns whether or not the header checksum is valid
    def _check_header_checksum(self):
        checksum = 0
        for i in range(0x134, 0x14D):
            checksum = checksum - self.data[i] - 1
        return checksum & 0xFF == self.data[0x14D]

    #Returns whether or not the global checksum is valid
    def _check_global_checksum(self):
        checksum = (sum(self.data) - sum(self.data[0x14E:0x150])) & 0xFFFF
        return checksum == (self.data[0x14E] << 8) + self.data[0x14F]

    #Disassembly helper functions

    #Prints a message and increments the index by n
    def p_inc(self, message, n):
        self.output.write(message + "\t;${:04X}\n".format(self.index))

        self.index += n

    def d8(self):
        return '${:02X}'.format(self.data[self.index + 1])

    def d16(self):
        f = '${:02X}{:02X}'
        return f.format(self.data[self.index + 1], self.data[self.index + 2])
    
    def a8(self):
        return self.d8()

    def a16(self):
        return self.d16()

    def r8(self):
        return self.d8()


    #Main entry point for disassembly
    def disassemble(self, output):
        self.output = output

        self.output.write("; Disassembled with github.com/awjnsn/gbdump\n")
        
        self.index = 0

        cb_instruction_table = {

            "0x0" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x1" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x2" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x3" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x4" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x5" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x6" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x7" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x8" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x9" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x10" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x11" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x12" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x13" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x14" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x15" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x16" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x17" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x18" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x19" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x1a" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x1b" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x1c" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x1d" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x1e" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x1f" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x20" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x21" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x22" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x23" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x24" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x25" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x26" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x27" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x28" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x29" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x2a" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x2b" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x2c" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x2d" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x2e" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x2f" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x30" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x31" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x32" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x33" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x34" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x35" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x36" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x37" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x38" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x39" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x3a" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x3b" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x3c" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x3d" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x3e" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x3f" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x40" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x41" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x42" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x43" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x44" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x45" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x46" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x47" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x48" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x49" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x4a" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x4b" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x4c" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x4d" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x4e" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x4f" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x50" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x51" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x52" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x53" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x54" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x55" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x56" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x57" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x58" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x59" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x5a" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x5b" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x5c" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x5d" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x5e" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x5f" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x60" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x61" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x62" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x63" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x64" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x65" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x66" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x67" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x68" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x69" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x6a" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x6b" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x6c" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x6d" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x6e" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x6f" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x70" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x71" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x72" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x73" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x74" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x75" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x76" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x77" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x78" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x79" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x7a" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x7b" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x7c" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x7d" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x7e" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x7f" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x80" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x81" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x82" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x83" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x84" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x85" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x86" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x87" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x88" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x89" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x8a" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x8b" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x8c" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x8d" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x8e" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x8f" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x90" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x91" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x92" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x93" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x94" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x95" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x96" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x97" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x98" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x99" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x9a" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x9b" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x9c" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x9d" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x9e" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0x9f" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa0" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa1" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa2" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa3" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa4" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa5" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa6" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa7" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa8" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xa9" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xaa" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xab" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xac" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xad" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xae" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xaf" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb0" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb1" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb2" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb3" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb4" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb5" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb6" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb7" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb8" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xb9" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xba" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xbb" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xbc" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xbd" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xbe" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xbf" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc0" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc1" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc2" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc3" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc4" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc5" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc6" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc7" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc8" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xc9" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xca" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xcb" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xcc" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xcd" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xce" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xcf" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd0" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd1" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd2" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd3" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd4" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd5" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd6" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd7" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd8" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xd9" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xda" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xdb" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xdc" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xdd" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xde" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xdf" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe0" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe1" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe2" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe3" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe4" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe5" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe6" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe7" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe8" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xe9" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xea" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xeb" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xec" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xed" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xee" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xef" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf0" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf1" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf2" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf3" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf4" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf5" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf6" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf7" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf8" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xf9" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xfa" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xfb" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xfc" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xfd" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xfe" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2),
            "0xff" : lambda: self.p_inc("; u cb instruction " + hex(self.data[self.index + 1]), 2)
        }

        instruction_table = {

            "0x0" : lambda: self.p_inc("nop", 1),
            "0x1" : lambda: self.p_inc("ld BC, " + self.d16(), 3),
            "0x2" : lambda: self.p_inc("ld [BC], a", 1),
            "0x3" : lambda: self.p_inc("inc BC", 1),
            "0x4" : lambda: self.p_inc("inc B", 1),
            "0x5" : lambda: self.p_inc("dec B", 1),
            "0x6" : lambda: self.p_inc("ld B, " + self.d8(), 2),
            "0x7" : lambda: self.p_inc("rcla", 1),
            "0x8" : lambda: self.p_inc("ld [" + self.a16() + "], SP" , 3),
            "0x9" : lambda: self.p_inc("add HL, BC", 1),
            "0xa" : lambda: self.p_inc("ld A, [BC]", 1),
            "0xb" : lambda: self.p_inc("dec BC", 1),
            "0xc" : lambda: self.p_inc("inc C", 1),
            "0xd" : lambda: self.p_inc("dec C", 1),
            "0xe" : lambda: self.p_inc("ld C, " + self.d8(), 2),
            "0xf" : lambda: self.p_inc("rrca", 1),

            "0x10" : lambda: self.p_inc("stop", 2),
            "0x11" : lambda: self.p_inc("ld DE, " + self.d16(), 3),
            "0x12" : lambda: self.p_inc("ld [DE], a", 1),
            "0x13" : lambda: self.p_inc("inc DE", 1),
            "0x14" : lambda: self.p_inc("inc D", 1),
            "0x15" : lambda: self.p_inc("dec D", 1),
            "0x16" : lambda: self.p_inc("ld D, " + self.d8(), 2),
            "0x17" : lambda: self.p_inc("rla", 1),
            "0x18" : lambda: self.p_inc("jr " + self.r8(), 2),
            "0x19" : lambda: self.p_inc("add HL, DE", 1),
            "0x1a" : lambda: self.p_inc("ld A, [DE]", 1),
            "0x1b" : lambda: self.p_inc("dec DE", 1),
            "0x1c" : lambda: self.p_inc("inc E", 1),
            "0x1d" : lambda: self.p_inc("dec E", 1),
            "0x1e" : lambda: self.p_inc("ld E, " + self.d8(), 2),
            "0x1f" : lambda: self.p_inc("rra", 1),
            
            "0x20" : lambda: self.p_inc("jr NZ, " + self.d8(), 2),
            "0x21" : lambda: self.p_inc("ld HL, " + self.d16(), 3),
            "0x22" : lambda: self.p_inc("ld [HL+], A", 1),
            "0x23" : lambda: self.p_inc("inc HL", 1),
            "0x24" : lambda: self.p_inc("inc H", 1),
            "0x25" : lambda: self.p_inc("dec H", 1),
            "0x26" : lambda: self.p_inc("ld H, " + self.d8(), 2),
            "0x27" : lambda: self.p_inc("daa", 1),
            "0x28" : lambda: self.p_inc("jr Z, " + self.r8(), 2),
            "0x29" : lambda: self.p_inc("add HL, HL", 1),
            "0x2a" : lambda: self.p_inc("ld A, [HL+]", 1),
            "0x2b" : lambda: self.p_inc("dec HL", 1),
            "0x2c" : lambda: self.p_inc("inc L", 1),
            "0x2d" : lambda: self.p_inc("dec L", 1),
            "0x2e" : lambda: self.p_inc("ld L, " + self.d8(), 2),
            "0x2f" : lambda: self.p_inc("cpl", 1),
            
            "0x30" : lambda: self.p_inc("jr NC, " + self.r8(), 2),
            "0x31" : lambda: self.p_inc("ld SP, " + self.d16(), 3),
            "0x32" : lambda: self.p_inc("ld [HL-], A", 1),
            "0x33" : lambda: self.p_inc("inc SP", 1),
            "0x34" : lambda: self.p_inc("inc [HL]", 1),
            "0x35" : lambda: self.p_inc("dec [HL]", 1),
            "0x36" : lambda: self.p_inc("ld [HL], " + self.d8(), 2),
            "0x37" : lambda: self.p_inc("scf", 1),
            "0x38" : lambda: self.p_inc("jr C, " + self.r8(), 2),
            "0x39" : lambda: self.p_inc("add HL, SP", 1),
            "0x3a" : lambda: self.p_inc("ld A, [HL-]", 1),
            "0x3b" : lambda: self.p_inc("dec SP", 1),
            "0x3c" : lambda: self.p_inc("inc A", 1),
            "0x3d" : lambda: self.p_inc("dec A", 1),
            "0x3e" : lambda: self.p_inc("ld A, " + self.d8(), 2),
            "0x3f" : lambda: self.p_inc("ccf", 1),
            
            "0x40" : lambda: self.p_inc("ld B, B", 1),
            "0x41" : lambda: self.p_inc("ld B, C", 1),
            "0x42" : lambda: self.p_inc("ld B, D", 1),
            "0x43" : lambda: self.p_inc("ld B, E", 1),
            "0x44" : lambda: self.p_inc("ld B, H", 1),
            "0x45" : lambda: self.p_inc("ld B, L", 1),
            "0x46" : lambda: self.p_inc("ld B, [HL]", 1),
            "0x47" : lambda: self.p_inc("ld B, A", 1),
            "0x48" : lambda: self.p_inc("ld C, B", 1),
            "0x49" : lambda: self.p_inc("ld C, C", 1),
            "0x4a" : lambda: self.p_inc("ld C, D", 1),
            "0x4b" : lambda: self.p_inc("ld C, E", 1),
            "0x4c" : lambda: self.p_inc("ld C, H", 1),
            "0x4d" : lambda: self.p_inc("ld C, L", 1),
            "0x4e" : lambda: self.p_inc("ld C, [HL]", 1),
            "0x4f" : lambda: self.p_inc("ld C, A", 1),
            
            "0x50" : lambda: self.p_inc("ld D, B", 1),
            "0x51" : lambda: self.p_inc("ld D, C", 1),
            "0x52" : lambda: self.p_inc("ld D, D", 1),
            "0x53" : lambda: self.p_inc("ld D, E", 1),
            "0x54" : lambda: self.p_inc("ld D, H", 1),
            "0x55" : lambda: self.p_inc("ld D, L", 1),
            "0x56" : lambda: self.p_inc("ld D, [HL]", 1),
            "0x57" : lambda: self.p_inc("ld D, A", 1),
            "0x58" : lambda: self.p_inc("ld E, B", 1),
            "0x59" : lambda: self.p_inc("ld E, C", 1),
            "0x5a" : lambda: self.p_inc("ld E, D", 1),
            "0x5b" : lambda: self.p_inc("ld E, E", 1),
            "0x5c" : lambda: self.p_inc("ld E, H", 1),
            "0x5d" : lambda: self.p_inc("ld E, L", 1),
            "0x5e" : lambda: self.p_inc("ld E, [HL]", 1),
            "0x5f" : lambda: self.p_inc("ld E, A", 1),
            
            "0x60" : lambda: self.p_inc("ld H, B", 1),
            "0x61" : lambda: self.p_inc("ld H, C", 1),
            "0x62" : lambda: self.p_inc("ld H, D", 1),
            "0x63" : lambda: self.p_inc("ld H, E", 1),
            "0x64" : lambda: self.p_inc("ld H, H", 1),
            "0x65" : lambda: self.p_inc("ld H, L", 1),
            "0x66" : lambda: self.p_inc("ld H, [HL]", 1),
            "0x67" : lambda: self.p_inc("ld H, A", 1),
            "0x68" : lambda: self.p_inc("ld L, B", 1),
            "0x69" : lambda: self.p_inc("ld L, C", 1),
            "0x6a" : lambda: self.p_inc("ld L, D", 1),
            "0x6b" : lambda: self.p_inc("ld L, E", 1),
            "0x6c" : lambda: self.p_inc("ld L, H", 1),
            "0x6d" : lambda: self.p_inc("ld L, L", 1),
            "0x6e" : lambda: self.p_inc("ld L, [HL]", 1),
            "0x6f" : lambda: self.p_inc("ld L, A", 1),

            "0x70" : lambda: self.p_inc("ld [HL], B", 1),
            "0x71" : lambda: self.p_inc("ld [HL], C", 1),
            "0x72" : lambda: self.p_inc("ld [HL], D", 1),
            "0x73" : lambda: self.p_inc("ld [HL], E", 1),
            "0x74" : lambda: self.p_inc("ld [HL], H", 1),
            "0x75" : lambda: self.p_inc("ld [HL], L", 1),
            "0x76" : lambda: self.p_inc("halt, ", 1),
            "0x77" : lambda: self.p_inc("ld [HL], A", 1),
            "0x78" : lambda: self.p_inc("ld A, B", 1),
            "0x79" : lambda: self.p_inc("ld A, C", 1),
            "0x7a" : lambda: self.p_inc("ld A, D", 1),
            "0x7b" : lambda: self.p_inc("ld A, E", 1),
            "0x7c" : lambda: self.p_inc("ld A, H", 1),
            "0x7d" : lambda: self.p_inc("ld A, L", 1),
            "0x7e" : lambda: self.p_inc("ld A, [HL]", 1),
            "0x7f" : lambda: self.p_inc("ld A, A", 1),
            
            "0x80" : lambda: self.p_inc("add A, B", 1),
            "0x81" : lambda: self.p_inc("add A, C", 1),
            "0x82" : lambda: self.p_inc("add A, D", 1),
            "0x83" : lambda: self.p_inc("add A, E", 1),
            "0x84" : lambda: self.p_inc("add A, H", 1),
            "0x85" : lambda: self.p_inc("add A, L", 1),
            "0x86" : lambda: self.p_inc("add A, [HL]", 1),
            "0x87" : lambda: self.p_inc("add A, A", 1),
            "0x88" : lambda: self.p_inc("adc A, B", 1),
            "0x89" : lambda: self.p_inc("adc A, C", 1),
            "0x8a" : lambda: self.p_inc("adc A, D", 1),
            "0x8b" : lambda: self.p_inc("adc A, E", 1),
            "0x8c" : lambda: self.p_inc("adc A, H", 1),
            "0x8d" : lambda: self.p_inc("adc A, L", 1),
            "0x8e" : lambda: self.p_inc("adc A, [HL]", 1),
            "0x8f" : lambda: self.p_inc("adc A, A", 1),
            
            "0x90" : lambda: self.p_inc("sub B", 1),
            "0x91" : lambda: self.p_inc("sub C", 1),
            "0x92" : lambda: self.p_inc("sub D", 1),
            "0x93" : lambda: self.p_inc("sub E", 1),
            "0x94" : lambda: self.p_inc("sub H", 1),
            "0x95" : lambda: self.p_inc("sub L", 1),
            "0x96" : lambda: self.p_inc("sub [HL]", 1),
            "0x97" : lambda: self.p_inc("sub A", 1),
            "0x98" : lambda: self.p_inc("sbc A, B", 1),
            "0x99" : lambda: self.p_inc("sbc A, C", 1),
            "0x9a" : lambda: self.p_inc("sbc A, D", 1),
            "0x9b" : lambda: self.p_inc("sbc A, E", 1),
            "0x9c" : lambda: self.p_inc("sbc A, H", 1),
            "0x9d" : lambda: self.p_inc("sbc A, L", 1),
            "0x9e" : lambda: self.p_inc("sbc A, [HL]", 1),
            "0x9f" : lambda: self.p_inc("sbc A, A", 1),
            
            "0xa0" : lambda: self.p_inc("and B", 1),
            "0xa1" : lambda: self.p_inc("and C", 1),
            "0xa2" : lambda: self.p_inc("and D", 1),
            "0xa3" : lambda: self.p_inc("and E", 1),
            "0xa4" : lambda: self.p_inc("and H", 1),
            "0xa5" : lambda: self.p_inc("and L", 1),
            "0xa6" : lambda: self.p_inc("and [HL]", 1),
            "0xa7" : lambda: self.p_inc("and A", 1),
            "0xa8" : lambda: self.p_inc("xor B", 1),
            "0xa9" : lambda: self.p_inc("xor C", 1),
            "0xaa" : lambda: self.p_inc("xor D", 1),
            "0xab" : lambda: self.p_inc("xor E", 1),
            "0xac" : lambda: self.p_inc("xor H", 1),
            "0xad" : lambda: self.p_inc("xor L", 1),
            "0xae" : lambda: self.p_inc("xor [HL]", 1),
            "0xaf" : lambda: self.p_inc("xor A", 1),
            
            "0xb0" : lambda: self.p_inc("or B", 1),
            "0xb1" : lambda: self.p_inc("or C", 1),
            "0xb2" : lambda: self.p_inc("or D", 1),
            "0xb3" : lambda: self.p_inc("or E", 1),
            "0xb4" : lambda: self.p_inc("or H", 1),
            "0xb5" : lambda: self.p_inc("or L", 1),
            "0xb6" : lambda: self.p_inc("or [HL]", 1),
            "0xb7" : lambda: self.p_inc("or A", 1),
            "0xb8" : lambda: self.p_inc("cp B", 1),
            "0xb9" : lambda: self.p_inc("cp C", 1),
            "0xba" : lambda: self.p_inc("cp D", 1),
            "0xbb" : lambda: self.p_inc("cp E", 1),
            "0xbc" : lambda: self.p_inc("cp H", 1),
            "0xbd" : lambda: self.p_inc("cp L", 1),
            "0xbe" : lambda: self.p_inc("cp [HL]", 1),
            "0xbf" : lambda: self.p_inc("cp A", 1),
            
            "0xc0" : lambda: self.p_inc("ret NZ", 1),
            "0xc1" : lambda: self.p_inc("pop BC", 1),
            "0xc2" : lambda: self.p_inc("jp NZ, " + self.a16(), 3),
            "0xc3" : lambda: self.p_inc("jp " + self.a16(), 3),
            "0xc4" : lambda: self.p_inc("call NZ, " + self.a16(), 3),
            "0xc5" : lambda: self.p_inc("push BC", 1),
            "0xc6" : lambda: self.p_inc("add A, " + self.d8(), 2),
            "0xc7" : lambda: self.p_inc("rst $00", 1),
            "0xc8" : lambda: self.p_inc("ret Z", 1),
            "0xc9" : lambda: self.p_inc("ret", 1),
            "0xca" : lambda: self.p_inc("jp Z, " + self.a16(), 3),
            "0xcb" : cb_instruction_table[hex(self.data[self.index + 1])],
            "0xcc" : lambda: self.p_inc("call Z, " + self.a16(), 3),
            "0xcd" : lambda: self.p_inc("call " + self.a16(), 3),
            "0xce" : lambda: self.p_inc("adc A, " + self.d8(), 2),
            "0xcf" : lambda: self.p_inc("rst $08", 1),
            
            "0xd0" : lambda: self.p_inc("ret NC", 1),
            "0xd1" : lambda: self.p_inc("pop DE", 1),
            "0xd2" : lambda: self.p_inc("jp NC, " + self.a16(), 3),
            #"0xd3" : lambda: self.p_inc(";SKIP REMOVE AFTER CB", 1),
            "0xd4" : lambda: self.p_inc("call NC, " + self.a16(), 3),
            "0xd5" : lambda: self.p_inc("push DE", 1),
            "0xd6" : lambda: self.p_inc("sub " + self.d8(), 2),
            "0xd7" : lambda: self.p_inc("rst $10", 1),
            "0xd8" : lambda: self.p_inc("ret C", 1),
            "0xd9" : lambda: self.p_inc("reti", 1),
            "0xda" : lambda: self.p_inc("jp C, " + self.a16(), 3),
            #"0xdb" : lambda: self.p_inc("; u instruction " + hex(self.data[self.index]), 1),
            "0xdc" : lambda: self.p_inc("call C, " + self.a16(), 3),
            #"0xdd" : lambda: self.p_inc("; u instruction " + hex(self.data[self.index]), 1),
            "0xde" : lambda: self.p_inc("sbc A, " + self.d8(), 2),
            "0xdf" : lambda: self.p_inc("rst $18", 1),
            
            "0xe0" : lambda: self.p_inc("ldh [" + self.a8() + "], A", 2),
            "0xe1" : lambda: self.p_inc("pop HL", 1),
            "0xe2" : lambda: self.p_inc("ld [C], A", 2), #Unsure why 2 long
            #"0xe3" : lambda: self.p_inc("; u instruction " + hex(self.data[self.index]), 1),
            #"0xe4" : lambda: self.p_inc("; u instruction " + hex(self.data[self.index]), 1),
            "0xe5" : lambda: self.p_inc("push HL", 1),
            "0xe6" : lambda: self.p_inc("and " + self.d8(), 2),
            "0xe7" : lambda: self.p_inc("rst $20", 1),
            "0xe8" : lambda: self.p_inc("add SP, " + self.r8(), 2),
            "0xe9" : lambda: self.p_inc("jp [HL]", 1),
            "0xea" : lambda: self.p_inc("ld [" + self.a16() + "], A", 3),
            #"0xeb" : lambda: self.p_inc("; u instruction " + hex(self.data[self.index]), 1),
            #"0xec" : lambda: self.p_inc("; u instruction " + hex(self.data[self.index]), 1),
            #"0xed" : lambda: self.p_inc("; u instruction " + hex(self.data[self.index]), 1),
            "0xee" : lambda: self.p_inc("xor " + self.d8(), 2),
            "0xef" : lambda: self.p_inc("rst $28", 1),
            
            "0xf0" : lambda: self.p_inc("ldh A, [" + self.a8() + "]", 2),
            "0xf1" : lambda: self.p_inc("pop AF", 1),
            "0xf2" : lambda: self.p_inc("ld A, [C]", 2),
            "0xf3" : lambda: self.p_inc("di", 1),
            #"0xf4" : lambda: self.p_inc("; u instruction " + hex(self.data[self.index]), 1),
            "0xf5" : lambda: self.p_inc("push af", 1),
            "0xf6" : lambda: self.p_inc("or " + self.d8(), 2),
            "0xf7" : lambda: self.p_inc("rst $30", 1),
            "0xf8" : lambda: self.p_inc("ld HL, SP+" + self.r8(), 2),
            "0xf9" : lambda: self.p_inc("ld SP, HL", 1),
            "0xfa" : lambda: self.p_inc("ld A, [" + self.a16() + "]", 3),
            "0xfb" : lambda: self.p_inc("ei", 1),
            #"0xfc" : lambda: self.p_inc("; u instruction " + hex(self.data[self.index]), 1),
            #"0xfd" : lambda: self.p_inc("; u instruction " + hex(self.data[self.index]), 1),
            "0xfe" : lambda: self.p_inc("cp " + self.d8(), 2),
            "0xff" : lambda: self.p_inc("rst $38", 1)
        }
        
        #While there is still more to disassemble
        while self.index < len(self.data):
            #Skip the header
            if self.index == 0x104:
                self.index = 0x150
            try:
                instruction_table[hex(self.data[self.index])]()
            except KeyError:
                self.output.write("; Misread instruction ")
                self.output.write(hex(self.data[self.index]) + " at ")
                self.output.write(hex(self.index) + "\n")
                self.index += 1
            