def detect_aes_128_ecb(input_file):
    lines = [line.strip("\n") for line in open(input_file).readlines()]
    block_size = 16 # bytes
    
    for line in lines:
        blocks = []
        i = 0

        while i < len(line):
            blocks.append(line[i:i+(2*block_size)])
            i += 32

        # If the plain text line was encoded with AES ECB, there will be 
        # at least one 16 byte block that was repeated (assuming there is a
        # repeated block in one of the lines) 

        if len(blocks) == len(set(blocks)):
            continue
        else:
            return line, blocks, lines.index(line)

# It is the 132nd line 