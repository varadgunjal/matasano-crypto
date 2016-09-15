from binascii import unhexlify
from base64 import b64encode

input_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

binary_string = unhexlify(input_string)
encoded = b64encode(binary_string)
print(encoded)
