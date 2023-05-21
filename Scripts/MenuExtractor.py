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

offset = 43644510
offset2 = 49926027
images_count = 8
images_count2 = 18
images = []

if not os.path.exists('extracted/menus/sprites'):
    os.makedirs('extracted/menus/sprites')

def read_image(image_offset):
    data = file[image_offset:image_offset + size]
    a = np.frombuffer(data, dtype='<u2')
    b = np.divmod((a), 2048)
    image = np.rint(np.vstack((b[0], np.divmod(b[1], 32))).T * np.array([[8.225, 4.05, 8.225]]))

    i = np.asarray(image).reshape((height, width, 3)).astype(np.uint8)
    images.append(Image.fromarray(i))

def define_palette(cores, palette_offset, data):
    palette = []
    for _ in range(cores):
        byte1 = bin(data[palette_offset])[2:].zfill(8)
        byte2 = bin(data[palette_offset+1])[2:].zfill(8)
        
        bit16 = (byte2 + byte1)

        r = round(int(bit16[:5], 2) * 8.225)
        g = round(int(bit16[5:11], 2) * 4.05)
        b = round(int(bit16[11:], 2) * 8.225)

        palette.append([r, g, b, 255])
        palette_offset += 2

    return palette

def read_sprite(image_offset, width, height, palette, name, sprites):
    image = np.zeros((height, width, 4))
    x = 0
    y = 0
    while True:
        jumper = sprites[image_offset:image_offset+5]
        y_jump = int.from_bytes(jumper[0:2], 'little', signed=True)
        x_jump = int.from_bytes(jumper[2:4], 'little', signed=True) // 2
        next_jumper = jumper[4]
        image_offset += 5
        if jumper == b'\xff\xff\xff\xff\xff':
            break

        x += x_jump
        y += y_jump
        for _ in range(next_jumper):
            image[y][x] = palette[sprites[image_offset]]
            x += 1
            image_offset += 1

    i = np.asarray(image[:]).reshape((height, width, 4)).astype(np.uint8)
    image  = Image.fromarray(i)
    image.save(f'extracted/menus/sprites/{name}.png')

sprites_count = int.from_bytes(file[offset+12:offset+16], 'little')
sprites_size = int.from_bytes(file[offset+16:offset+20], 'little')
offset += 20

for x in range(images_count):
    print(f'Lendo Imagem {x}')
    width = int.from_bytes(file[offset:offset+4], 'little')
    height = int.from_bytes(file[offset+4:offset+8], 'little')
    width = width * int.from_bytes(file[offset+8:offset+12], 'little')
    height = height * int.from_bytes(file[offset+12:offset+16], 'little')
    size = width * height * 2
    read_image(offset + 20)
    offset += size + 20

header = 54360
sprites = file[offset:offset+header+sprites_size]
palette = []
current_palette = None
sprites_offset = 0
print('Extracting Sprites')
for n in range(sprites_count):
    image_offset = int.from_bytes(sprites[sprites_offset:sprites_offset+4], 'little') + header
    palette_offset = int.from_bytes(sprites[sprites_offset+4:sprites_offset+8], 'little') + header
    width = int.from_bytes(sprites[sprites_offset+8:sprites_offset+12], 'little')
    height = int.from_bytes(sprites[sprites_offset+12:sprites_offset+16], 'little')
    cores = int.from_bytes(sprites[sprites_offset+16:sprites_offset+20], 'little')

    if palette_offset != current_palette:
        palette = define_palette(256, palette_offset, sprites)
        current_palette = palette_offset

    if n != 2613:
        read_sprite(image_offset, width, height, palette, str(n).zfill(4), sprites)

    sprites_offset += 20

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


for n, x in enumerate(images):
    x.save(f'extracted/menus/{str(n).zfill(2)}.png')

print('Finished (Terminado)')
