# by: Edu371
# Extrai PICT_*_*
# Extracts PICT_*_*

import os
import numpy as np
from PIL import Image

file_name = 'Outlive.dat'

file = open(file_name, 'rb')
file = file.read()

file = file[113971525:142379241]
file_size = len(file)


names = ['PICT_INIT',
         'PICT_MAIN_640', 'PICT_MAIN_800', 'PICT_MAIN_1024',
         'PICT_MULTI_640', 'PICT_MULTI_800', 'PICT_MULTI_1024',
         'PICT_HUMAN_640', 'PICT_HUMAN_800', 'PICT_HUMAN_1024',
         'PICT_ROBOT_640', 'PICT_ROBOT_800', 'PICT_ROBOT_1024',
         'PICT_COOP_640', 'PICT_COOP_800', 'PICT_COOP_1024']


if not os.path.exists('extracted/pict'):
    os.makedirs('extracted/pict')

def read_image(image_offset, width, height, name):
    size = width * height * 2
    data = file[image_offset:image_offset + size]
    image = []
    for c in range(0, size, 2):
        byte1 = bin(data[c])[2:].zfill(8)
        byte2 = bin(data[c+1])[2:].zfill(8)

        bit16 = (byte2 + byte1)
        
        r = round(int(bit16[:5], 2) * 8.225)
        g = round(int(bit16[5:11], 2) * 4.05)
        b = round(int(bit16[11:], 2) * 8.225)

        image.append([r, g, b])

    i = np.asarray(image).reshape((height, width, 3)).astype(np.uint8)
    image = Image.fromarray(i)
    image.save(f'extracted/pict/{name}.png')
    print(f'saved {name}.png')

print('Started (Iniciado)')

offset = 0
n = 0
while offset != file_size:
    images_count = int.from_bytes(file[offset:offset+4], 'little')
    header_size = 12 + images_count * 12
    size = int.from_bytes(file[offset+4:offset+8], 'little') + header_size
    bpp = int.from_bytes(file[offset+8:offset+12], 'little')
    current_offset = offset
    offset += 12
    for x in range(images_count):
        image_offset = int.from_bytes(file[offset:offset+4], 'little') + header_size + current_offset
        width = int.from_bytes(file[offset+4:offset+8], 'little')
        height = int.from_bytes(file[offset+8:offset+12], 'little')
        read_image(image_offset, width, height, f'{names[n]}_{str(x).zfill(2)}')
        offset += 12
    n += 1
    offset = image_offset + width * height * 2

print('Finished (Terminado)')
