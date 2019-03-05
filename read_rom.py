#!/usr/bin/env python3

from sys import argv #For reading command line arguments
import cart #Cartridge class

def main():
    if len(argv) is 3:
        rom = cart.ROM(open(argv[1], "rb").read())
        output = open(argv[2], "w")

        output.write("; Disassembled with https://github.com/awjnsn/gbdump");
    else:
        print("Usage: " + argv[0] + " rom_file output_file")

  
if __name__== "__main__":
    main()
