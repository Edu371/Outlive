# by: Edu371
# Extrai GRAPH_INT_*_*
# Extracts GRAPH_INT_*_*

import os
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


if not os.path.exists('extracted/graph'):
    os.makedirs('extracted/graph')

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
    image.save(f'extracted/graph/{name}.png')
    print(f'saved {name}.png')

print('Started (Iniciado)')

for section in sections:
    offset = section[0]
    name = section[1]
    if not os.path.exists(f'extracted/graph/{name}'):
        os.makedirs(f'extracted/graph/{name}')
    
    images_count = int.from_bytes(file[offset+4:offset+8], 'little')
    header_size = 20
    
    offset += 20
    for x in range(images_count):
        width = int.from_bytes(file[offset:offset+4], 'little') * int.from_bytes(file[offset+8:offset+12], 'little')
        height = int.from_bytes(file[offset+4:offset+8], 'little') * int.from_bytes(file[offset+12:offset+16], 'little')
        offset += 20
        read_image(offset, width, height, f'{name}/{str(x).zfill(2)}')
        offset += width * height * 2
        
print('Finished (Terminado)')
