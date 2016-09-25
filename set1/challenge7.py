from Crypto.Cipher import AES
from base64 import b64decode

key = "YELLOW SUBMARINE"

def aes_128_ecb_decrypt(input_file):
    cipher_text = open(input_file).read()
    cipher_text = b64decode(cipher_text)

    decoder = AES.new(key, AES.MODE_ECB)
    plain_text = decoder.decrypt(cipher_text)

    return plain_text