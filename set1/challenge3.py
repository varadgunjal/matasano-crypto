from binascii import hexlify, unhexlify
from itertools import cycle
import string

byte_passwords = [format(i, "#04x")[2:] for i in range(1, 256)]

# ETAOIN SHRDLU

# Cooking MC's like a pound of bacon, Key : 0x58
# Ice Ice Baby!
cipher = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

# Python 2.x
def xor_hex_strings_2(s1, s2):
    return hexlify(''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in 
                    zip(unhexlify(s1), cycle(unhexlify(s2)))))

# Python 3.x
def xor_hex_strings_3(s1, s2):
    return ''.join([hex(int(s1, 16) ^ int(s2, 16))[2:] 
                    for s1, s2 in zip(s1, cycle(s2))])

def crack_single_byte_xor(cipher_text):   
    for password in byte_passwords:        
        text_hex = xor_hex_strings_3(cipher_text, password)    

        # Python 2.x    
        # text = text_hex.decode("hex")

        # Python 3
        # can't decode some bytes with this
        text = bytes.fromhex(text_hex).decode("utf-8", "ignore")  

        valid = True
        for char in text:
            if char not in string.printable:
                valid = False
                break

        if valid:
            print(text, ", ", password)

# crack_single_byte_xor(cipher)

def single_byte_xor_for_multi_byte_key(most_common_bytes):

    most_probable_byte_password = None
    max_matching_chars = 0
    
    for password in byte_passwords:
        # For each byte in most_common_bytes, xor with a candidate byte 
        # password.  Convert the output bytes to ascii / utf-8 and verify how
        # many, if any, match with ETAOIN[space]SHRDLU

        chars_match = 0

        for cipher_byte in most_common_bytes:
            character = chr(int(cipher_byte, 16) ^ int(password, 16))
            if character in "etaoin shrdlu":
                chars_match += 1
        
        if chars_match > max_matching_chars:
            max_matching_chars = chars_match
            most_probable_byte_password = password

    return most_probable_byte_password
