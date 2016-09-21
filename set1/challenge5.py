#!/usr/bin/python

from challenge3 import xor_hex_strings_2, xor_hex_strings_3
from binascii import hexlify
import sys

input_text = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
cipher_key = "ICE"

# Python 2
def multi_byte_xor_encode_2(input_text, cipher_key):
    input_hex = input_text.encode("hex")
    key_hex = cipher_key.encode("hex")

    cipher_text = xor_hex_strings_2(input_hex, key_hex)    
    print(cipher_text)  

# Python 3
def convert_char_string_to_hex_3(s):
    byte_array = bytes(s, "utf-8")
    hex_string = hexlify(byte_array).decode("utf-8")

    return hex_string

def multi_byte_xor_encode_3(input_text, cipher_key):
    input_hex = convert_char_string_to_hex_3(input_text)
    key_hex = convert_char_string_to_hex_3(cipher_key)

    cipher_text = xor_hex_strings_3(input_hex, key_hex)    
    print(cipher_text) 

# multi_byte_xor_encode_3(input_text, cipher_key)