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
def multi_byte_xor_encode_3(input_text, cipher_key):
    input_byte_array = bytes(input_text, "utf-8")
    input_hex = hexlify(input_byte_array).decode("utf-8")

    key_byte_array = bytes(cipher_key, "utf-8")
    key_hex = hexlify(key_byte_array).decode("utf-8")

    cipher_text = xor_hex_strings_3(input_hex, key_hex)    
    print(cipher_text) 


multi_byte_xor_encode_3(input_text, cipher_key)