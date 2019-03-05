from enum import Enum

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

    #Internal data retrieval functions 

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
