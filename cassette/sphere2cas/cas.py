#!/usr/bin/env python3
# cas.py
#
# Author : Andrew Shapton 
# Copyright (C) 2023
#
# Requires Python 3.9 or newer
#

"""
Takes a binary Sphere-1 program and converts it into a format that can be
sent to a program that encodes it into a Kansas City Standard WAV file,
that when played will be readable by the cassette tape interface on a 
Sphere-1 computer.
See http://en.wikipedia.org/wiki/Kansas_City_standard
"""

# Open the binary file for reading
with open('pds-v3n.bin', 'rb') as file:
    binary_data = file.read()

# Get length of the program to store in bytes minus 1
raw_data = len(binary_data) - 1;

with open('output','wb') as file:
    # Write the 3 synchronisation bytes
    file.write(0x16.to_bytes(1,'big'));
    file.write(0x16.to_bytes(1,'big'));
    file.write(0x16.to_bytes(1,'big'));
    
    # Write the 1 byte constant marker
    file.write(0x1B.to_bytes(1,'big'));
    
    # Write the count of bytes in the block (high byte first)
    file.write(raw_data.to_bytes(2,'big'));
    
    # Write the 2 character block name    
    file.write(bytes('AB','ascii'));
    
    # Initialise checksum
    checksum = 0;
    # Write raw data to the file
    for x in binary_data:
        file.write(x.to_bytes(1,'big'));
        checksum = checksum + x;

    # Write the end of transmission byte
    file.write(0x17.to_bytes(1,'big'));
    
    # Checksum is the summation of the bytes in the program MOD 256
    checksum = (checksum % 256);
    
    # Write the checksum byte
    file.write(checksum.to_bytes(1,'big'));
    
    # Write the 3 final trailer bytes (actually the checksum written 3 times)
    file.write(checksum.to_bytes(1,'big'));
    file.write(checksum.to_bytes(1,'big'));
    file.write(checksum.to_bytes(1,'big'));
    
    


