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
        text = bytes.fromhex(text_hex).decode("utf-8", "ignore")  # can't decode some bytes with this

        valid = True
        for char in text:
            if char not in string.printable:
                valid = False
                break

        if valid and " " in text:
            print(text, ", ", password)

# crack_single_byte_xor(cipher)

# def single_byte_xor_for_multi_byte_key(cipher_text):
#     ascii_frequency = []
#     for password in byte_passwords:
#         text_hex = xor_hex_strings(cipher_text, password)        
#         text = text_hex.decode("hex")
#         frequency = 0

#         for char in text:
#             if char in string.printable:
#                 frequency += 1

#         ascii_frequency.append((password, frequency))
        
#         # print text, ", ", password
#         # time.sleep(1)

#     # return password corresponding to max ascii character frequency
#     # print ascii_frequency
#     return sorted(ascii_frequency, key=lambda x:x[1], reverse=True)[0][0]