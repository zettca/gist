import os
import sys
import struct
from PIL import Image

def get_bit(byte, i):
    mask = 1 << i
    return 1 if byte & mask else 0

def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b)

def extract(imgFile, password):
    img = Image.open(imgFile)
    width, height = img.size
    img_size = os.stat(imgFile).st_size
    img_data = img.convert('RGBA').getdata()
    offset = int(password) % 13

    bit_string = ""
    j = 0
    for h in range(height):
        for w in range(width):
            if j < offset:
                j = j + 1
                continue

            r, g, b, a = img_data.getpixel((w, h))

            bit_string += str(get_bit(r, 0)) + str(get_bit(r, 1))
            bit_string += str(get_bit(g, 0)) + str(get_bit(g, 1))
            bit_string += str(get_bit(b, 0)) + str(get_bit(b, 1))

    steg_header = [int(bit_string[b:b+8], 2) for b in range(0, 4*8, 8)]
    steg_len = 0
    for i in range(len(steg_header)):
        steg_len += steg_header[i] * 256**i

    #print(steg_len)
    if len(sys.argv) > 3 and sys.argv[3] == "len":
        return steg_len

    steg_body_bits = bit_string[8*4:8*(steg_len+4)] # steg body

    byte_i = 0
    steg_body_string = ""
    for bi in range(steg_len):
        bits = steg_body_bits[8*bi:8*(bi+1)]
        steg_body_string += chr(int(bits, 2))

    return steg_body_string

res = extract(sys.argv[1], sys.argv[2])
print(res)
