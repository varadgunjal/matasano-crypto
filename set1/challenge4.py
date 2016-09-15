from challenge3 import single_byte_xor

input_file = "4.txt"
hex_strings = [x.strip("\n") for x in open(input_file).readlines()]

for hex_string in hex_strings:
    print(hex_string)
    single_byte_xor(hex_string)
    print("\n")