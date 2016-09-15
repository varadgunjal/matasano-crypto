from itertools import cycle
from binascii import hexlify, unhexlify

s1 = "1c0111001f010100061a024b53535009181c"
s2 = "686974207468652062756c6c277320657965"

# Python 2.x solution because binascii is a little bitch in Python 3
print(hexlify(''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in 
                zip(unhexlify(s1), cycle(unhexlify(s2))))))