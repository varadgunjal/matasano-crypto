from challenge3 import xor_hex_strings

input_text = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
cipher_key = "ICE"

def multi_byte_xor_encode(input_text, cipher_key):
    input_hex = input_text.encode("hex")
    key_hex = cipher_key.encode("hex")

    cipher_text = xor_hex_strings(input_hex, key_hex)    
    print cipher_text    

multi_byte_xor_encode(input_text, cipher_key)

  



