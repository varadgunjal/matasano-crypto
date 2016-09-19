#!/usr/bin/python
from challenge3 import xor_hex_strings, single_byte_xor_for_multi_byte_key
from base64 import b64decode
import time

keysize_values = range(2, 100)

def calculate_hamming_distance_between(s1, s2):
    assert len(s1) == len(s2)
    
    s1 = s1.encode("hex")
    s2 = s2.encode("hex")

    count = 0

    z = xor_hex_strings(s1, s2)
    z = bin(int(z, 16))[2:]

    return z.count("1")

def decode_text(input_file):
    f = open(input_file).read()
    binary_encoding = b64decode(f)
    hex_encoding = binary_encoding.encode("hex") 

    return hex_encoding

def get_keysize(input_file):
    hex_encoding = decode_text(input_file)
    keysize_candidates = []

    for keysize in keysize_values:
        st_1, st_2 = hex_encoding[0:2*keysize], hex_encoding[2*keysize:4*keysize]
        hamming_distance = calculate_hamming_distance_between(st_1, st_2)
        keysize_candidates.append((keysize, (float) (hamming_distance / keysize)))

        print "Keysize : ", keysize, " Hamming Distance : ", hamming_distance, " Normalized : ", ((float) (hamming_distance / keysize)), "\n"

    possible_keysizes = sorted(keysize_candidates, key=lambda x: x[1])[:5]
    possible_keysizes = [k[0] for k in possible_keysizes]
    return possible_keysizes

def get_blocks_of_size(hex_code, keysize):
    blocks = []
    
    for i in range(0, len(hex_code) / (2 * keysize)):
        bytes_keysize = 2 * keysize
        start_index = i * bytes_keysize
        end_index = (i + 1) * bytes_keysize

        if end_index > len(hex_code):
            end_index = len(hex_code)

        block = hex_code[start_index:end_index]

        if len(block) == bytes_keysize:
            blocks.append(block)

    return blocks

def transpose(hex_code, keysize):
    bytes_keysize = 2 * keysize
    blocks = get_blocks_of_size(hex_code, keysize)
    transposed = []

    i = 0

    while i  < bytes_keysize:
        t = ''.join([block[i:i+2] for block in blocks])
        transposed.append(t)
        i += 2

    return transposed

def crack_blocks(hex_code, keysize):
    transposed = transpose(hex_code, keysize)
    key_bytes = []

    for t in transposed:
        probable_block_crack_byte = single_byte_xor_for_multi_byte_key(t)
        key_bytes.append(probable_block_crack_byte)

    probable_key = "".join(key_bytes)
    return probable_key

def crack_multi_byte_repeated_xor(input_file, keysize=0):
    hex_encoding = decode_text(input_file)

    if keysize != 0:
        probable_key = crack_blocks(hex_encoding, keysize)
        text_hex = xor_hex_strings(hex_encoding, probable_key) 
        text = text_hex.decode("hex")

        print "\n\nKeysize\t:\t", keysize, "\nKey\t:\t", probable_key, "\nText\t:\t", text
    
    else:
        # possible_keysizes = get_keysize(input_file)

        for keysize in range(2, 100):
            probable_key = crack_blocks(hex_encoding, keysize)
            text_hex = xor_hex_strings(hex_encoding, probable_key) 
            text = text_hex.decode("hex")
            print "\n\nKeysize\t:\t", keysize, "\nKey\t:\t", probable_key, "\nDecoded Text\t:\t", text

            time.sleep(5)



s1 = "this is a test"
s2 = "wokka wokka!!!"
print calculate_hamming_distance_between(s1, s2)

# print get_keysize("6.txt")

