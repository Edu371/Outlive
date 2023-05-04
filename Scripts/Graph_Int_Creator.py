# by: Edu371
# Insere GRAPH_INT_*_*
# Inserts GRAPH_INT_*_*

import os
from os import listdir
from os.path import isfile
import numpy as np
from PIL import Image

# file_name = 'Outlive.dat'
file_name = input('Outlive.dat(Path): ')

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
    image = np.asarray(Image.open(images[image_index]).getdata())[:,:3]
    data = np.sum(np.rint(image / np.array([8.225, 4.05, 8.225])
                          ).astype(int) * np.array([2048, 32, 1]), axis=1
                  ).astype('<u2').tobytes()

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
