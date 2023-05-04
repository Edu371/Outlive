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
    a = np.frombuffer(data, dtype='<u2')
    b = np.divmod((a), 2048)
    image = np.rint(np.vstack((b[0], np.divmod(b[1], 32))).T * np.array([[8.225, 4.05, 8.225]]))

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
