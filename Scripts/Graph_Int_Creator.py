# by: Edu371
# Insere GRAPH_INT_*_*
# Inserts GRAPH_INT_*_*

import os
from os import listdir
from os.path import isfile
import numpy as np
from PIL import Image

file_name = 'Outlive.dat'

file = open(file_name, 'rb')
file = file.read()

sections = [[142379241, 'GRAPH_INT_ROB_640'],
            [143990708, 'GRAPH_INT_ROB_800'],
            [146157931, 'GRAPH_INT_ROB_1024'],
            [149386862, 'GRAPH_INT_HUM_640'],
            [150998867, 'GRAPH_INT_HUM_800'],
            [153167035, 'GRAPH_INT_HUM_1024']]

path = input('Pasta(Path): ')
output_name = input('Saída(Output): ')
if '.dat' not in output_name:
    output_name += '.dat'

images = {}
files = []
for _, section in sections:
    files.extend([f'{section}/{f}' for f in listdir(f'{path}/{section}') if isfile(f'{path}/{section}/{f}')])
for a in files:
    if '.png' in a:
        images[a.replace('.png', '')] = f'{path}/{a}'

def convert_image(image_index, image_offset):
    global file
    image = Image.open(images[image_index]).getdata()
    data = b''
    for pixel in image:
        r = bin(round(pixel[0] / 8.225))[2:].zfill(5)
        g = bin(round(pixel[1] / 4.05))[2:].zfill(6)
        b = bin(round(pixel[2] / 8.225))[2:].zfill(5)

        bit16 = (r + g + b)

        byte1 = int(bit16[8:], 2).to_bytes(1, 'little')
        byte2 = int(bit16[:8], 2).to_bytes(1, 'little')
        data += byte1+byte2

    file = file[:image_offset] + data + file[image_offset + size:]

print('Started (Iniciado)')

for section in sections:
    offset = section[0]
    name = section[1]
    
    images_count = int.from_bytes(file[offset+4:offset+8], 'little')
    header_size = 20
    
    offset += 20
    for x in range(images_count):
        width = int.from_bytes(file[offset:offset+4], 'little') * int.from_bytes(file[offset+8:offset+12], 'little')
        height = int.from_bytes(file[offset+4:offset+8], 'little') * int.from_bytes(file[offset+12:offset+16], 'little')
        size = width * height * 2
        offset += 20
        if f'{name}/{str(x).zfill(2)}' in images:
            print(f'Convertendo Image {name}/{str(x).zfill(2)}.png')
            convert_image(f'{name}/{str(x).zfill(2)}', offset)
        offset += size

output = open(output_name, 'wb')
output.write(file)
output.close()
print('Finished (Terminado)')
