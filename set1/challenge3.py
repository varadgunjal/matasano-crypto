from binascii import hexlify, unhexlify
from itertools import cycle
import string

# ETAOIN SHRDLU

# Cooking MC's like a pound of bacon
# Ice Ice Baby!
cipher = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def xor_hex_strings(s1, s2):
    return hexlify(''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in 
                    zip(unhexlify(s1), cycle(unhexlify(s2)))))

def single_byte_xor_decode(cipher_text):
    for i in range(1, 256):
        password = format(i, "#04x")[2:]
        
        text_hex = xor_hex_strings(cipher_text, password)        
        text = text_hex.decode("hex")

        valid = True

        for char in text:
            if char not in string.printable:
                valid = False
                break

        if valid and " " in text:
            print text, password
