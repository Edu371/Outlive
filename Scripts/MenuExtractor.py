# by: Edu371
# Extrai Imagens de GRAPH_MENU
# Extracts Images from GRAPH_MENU

import numpy as np
from PIL import Image
import os

file_name = 'Outlive.dat'
print('Started (Iniciado)')

file = open(file_name, 'rb')
file = file.read()

offset = 43644530
offset2 = 49926027
images_count = 8
images_count2 = 18
images = []

def read_image(image_offset):
    data = file[image_offset:image_offset + size]
    image = []
    for n in range(0, len(data), 2):
        byte1 = bin(data[n])[2:].zfill(8)
        byte2 = bin(data[n+1])[2:].zfill(8)

        bit16 = (byte2 + byte1)
        
        r = round(int(bit16[:5], 2) * 8.225)
        g = round(int(bit16[5:11], 2) * 4.05)
        b = round(int(bit16[11:], 2) * 8.225)

        image.append([r, g, b])

    i = np.asarray(image).reshape((height, width, 3)).astype(np.uint8)
    images.append(Image.fromarray(i))


for x in range(images_count):
    print(f'Lendo Imagem {x}')
    width = int.from_bytes(file[offset:offset+4], 'little')
    height = int.from_bytes(file[offset+4:offset+8], 'little')
    width = width * int.from_bytes(file[offset+8:offset+12], 'little')
    height = height * int.from_bytes(file[offset+12:offset+16], 'little')
    size = width * height * 2
    read_image(offset + 20)
    offset += size + 20

offset = offset2
for x in range(images_count2):
    print(f'Lendo Imagem {images_count + x}')
    width = int.from_bytes(file[offset:offset+4], 'little')
    height = int.from_bytes(file[offset+4:offset+8], 'little')
    width = width * int.from_bytes(file[offset+8:offset+12], 'little')
    height = height * int.from_bytes(file[offset+12:offset+16], 'little')
    size = width * height * 2
    read_image(offset + 20)
    offset += size + 40

if not os.path.exists('extracted/menus'):
    os.makedirs('extracted/menus')

for n, x in enumerate(images):
    x.save(f'extracted/menus/{str(n).zfill(2)}.png')

print('Finished (Terminado)')
