#!/usr/bin/python
from challenge3 import xor_hex_strings_3, single_byte_xor_for_multi_byte_key
from challenge5 import convert_char_string_to_hex_3
from itertools import combinations
from statistics import mean
from binascii import hexlify
from base64 import b64decode

from collections import Counter

import time

keysize_values = range(2, 100)

def calculate_hamming_distance_between(s1, s2):
    assert len(s1) == len(s2)
    
    # Python 2.x
    # s1 = s1.encode("hex")
    # s2 = s2.encode("hex")

    # Python 3
    s1 = convert_char_string_to_hex_3(s1)
    s2 = convert_char_string_to_hex_3(s2)

    count = 0

    # z = xor_hex_strings_2(s1, s2)
    z = xor_hex_strings_3(s1, s2)
    z = bin(int(z, 16))[2:]

    return z.count("1")

def decode_text(input_file, b64=True):
    f = open(input_file).read()
    if b64:
        binary_encoding = b64decode(f)
    else:
        return f
    
    # Python 2.x
    # hex_encoding = binary_encoding.encode("hex")

    # Python 3.x
    hex_encoding = hexlify(binary_encoding).decode("utf-8") # need to return a                                                          # hex string
    return hex_encoding

def get_keysize(input_file, b64=True):
    hex_encoding = decode_text(input_file, b64)
    keysize_candidates = []

    # Estimate with 2 blocks 

    # for keysize in keysize_values:
    #     # each byte = 2 characters in the encoding
    #     st_1, st_2 = hex_encoding[0:2*keysize], \
    #                         hex_encoding[2*keysize:4*keysize]
    #     hamming_distance = calculate_hamming_distance_between(st_1, st_2)
    #     keysize_candidates.append((keysize, \
    #                         (float) (hamming_distance / keysize)))

    #     # print("Keysize : ", keysize, " Hamming Distance : ", hamming_distance, " Normalized : ", 
    #     #         ((float) (hamming_distance / keysize)), "\n")

    # possible_keysizes = sorted(keysize_candidates, key=lambda x: x[1])[:5]
    # possible_keysizes = [k[0] for k in possible_keysizes]
    # return possible_keysizes


    # Estimate with 4 blocks : Always a better option

    for keysize in keysize_values:
        st_1, st_2 = hex_encoding[0:2*keysize], hex_encoding[2*keysize:4*keysize]
        st_3, st_4 = hex_encoding[4*keysize:6*keysize], hex_encoding[6*keysize:8*keysize]

        pairs = combinations([st_1, st_2, st_3, st_4], 2)
        
        # For some weird reason, pair[0] wasn't working. 
        # Is pair a reserved word? 
        hamming_distance = [calculate_hamming_distance_between(p[0], p[1]) for p in pairs]        
        avg_hamming_distance = mean(hamming_distance)

        keysize_candidates.append((keysize, (float) (avg_hamming_distance / keysize)))

    possible_keysizes = sorted(keysize_candidates, key=lambda x: x[1])[:5]
    possible_keysizes = [k[0] for k in possible_keysizes]
    return possible_keysizes

def get_blocks_of_size(hex_code, keysize):
    blocks = []
    
    for i in range(0, len(hex_code) // (2 * keysize)):
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
        # Count the 13 most common bytes. With luck, they should 
        # correspond to ETAOIN[space]SHRDLU. Now we only consider those single 
        # byte keys which when xor-ed with each of these bytes gives
        # ETAOIN[space]SHRDLU, at least those which give the max percentage of
        # matches.

        split_t = [t[i:i+2] for i in range(0, len(t), 2)]
        most_common_bytes = [com[0] for com in Counter(split_t).most_common(13)]

        most_probable_block_crack_byte = \
                        single_byte_xor_for_multi_byte_key(most_common_bytes)
        key_bytes.append(most_probable_block_crack_byte)

    most_probable_key = "".join(key_bytes)
    return most_probable_key

# The probable keysizes for this text are 2, 5, 29 on
# analysis of hamming distance with 2 & 4 initial block sizes

# Change b64 to False for picoCTF or any non-bas 64 encoding
def crack_multi_byte_repeated_xor(input_file, keysize=0, b64=True):
    hex_encoding = decode_text(input_file, b64)

    # Optional keysize argument to test with various keysizes
    if keysize != 0:
        most_probable_key = crack_blocks(hex_encoding, keysize)
        text_hex = xor_hex_strings_3(hex_encoding, most_probable_key) 
        # text = text_hex.decode("hex")
        text = bytes.fromhex(text_hex).decode("utf-8", "ignore")

        print("\n\nKeysize\t:\t", keysize, "\nKey\t:\t", most_probable_key,             "\nText\t:\t", text)
    
    # the real deal
    else:
        # gotten from Hamming distance experiments
        possible_keysizes = (2, 5, 29)    # Matasano Crypto
        # possible_keysizes = (3, 21, 28)     # picoCTF 2014        

        for keysize in possible_keysizes:
            most_probable_key = crack_blocks(hex_encoding, keysize)
            text_hex = xor_hex_strings_3(hex_encoding, most_probable_key) 
            # text = text_hex.decode("hex")
            text = bytes.fromhex(text_hex).decode("utf-8", "ignore")

            print("\n\nKeysize\t:\t", keysize, "\nKey\t:\t", most_probable_key, "\nDecoded Text\t:\t", text)

            time.sleep(5)

# The Matasano guys have an unhealthy obsession with Vanilla Ice.
# The damn decryption is the lyrics of the song 'Play That Funky Music'.
# Final decryption : Length =  29 bytes
# Key = 5465726d696e61746f7220583a204272696e6720746865206e6f697365
