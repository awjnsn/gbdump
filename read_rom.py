#!/usr/bin/env python3

from sys import argv #For reading command line arguments
import cart #Cartridge class

def main():
    if len(argv) is 3:
        input_file = open(argv[1], "rb")
        output_file = open(argv[2], "w")
        
        rom = cart.ROM(input_file.read())
        rom.disassemble(output_file)

        input_file.close()
        output_file.close()

    else:
        print("Usage: " + argv[0] + " rom_file output_file")

  
if __name__== "__main__":
    main()
