# by: Edu371
# Extrai GRAPH_INT_*_*
# Extracts GRAPH_INT_*_*

import os
import numpy as np
from PIL import Image
from time import perf_counter

file_name = 'Outlive.dat'

file = open(file_name, 'rb')
file = file.read()

sections = [[142379241, 'GRAPH_INT_ROB_640'],
            [143990708, 'GRAPH_INT_ROB_800'],
            [146157931, 'GRAPH_INT_ROB_1024'],
            [149386862, 'GRAPH_INT_HUM_640'],
            [150998867, 'GRAPH_INT_HUM_800'],
            [153167035, 'GRAPH_INT_HUM_1024']]

sprites_file = file[4108:12481239]
simbolo_file = file[143982667:143990708]
subpaleta_file = file[12481239:13197983]

offset = 0
subpaleta = {}
subpaleta_count = int.from_bytes(subpaleta_file[0:4], 'little')
for var in range(subpaleta_count):
    offset = int.from_bytes(subpaleta_file[8+var*16:12+var*16], 'little') + 968
    palette_id = int.from_bytes(subpaleta_file[12+var*16:16+var*16], 'little')
    variations = int.from_bytes(subpaleta_file[16+var*16:20+var*16], 'little')
    colors = int.from_bytes(subpaleta_file[20+var*16:24+var*16], 'little') * 256
    subpaleta[palette_id] = [offset, variations, colors]

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
    image.save(f'extracted/graph/{name}.png')


special_palettes = {}
simbolo_count = int.from_bytes(simbolo_file[:4], 'little')
simbolo_offset = 4
for x in range(simbolo_count):
    a = simbolo_file[simbolo_offset]
    b = int.from_bytes(simbolo_file[simbolo_offset+1:simbolo_offset+5], 'little', signed=True) - 13121
    c = int.from_bytes(simbolo_file[simbolo_offset+5:simbolo_offset+7], 'little', signed=True)
    d = int.from_bytes(simbolo_file[simbolo_offset+7:simbolo_offset+11], 'little', signed=True) - 13121
    e = int.from_bytes(simbolo_file[simbolo_offset+11:simbolo_offset+15], 'little', signed=True)
    f = int.from_bytes(simbolo_file[simbolo_offset+15:simbolo_offset+19], 'little', signed=True) - 13121
    simbolo_offset += 19
    if not a:
        if c in subpaleta:
            palette = define_palette(256, subpaleta[c][0], subpaleta_file)
            special_palettes[b] = palette
            if f > 0:
                special_palettes[f] = palette

special_palettes[1291] = define_palette(256, 4921345, sprites_file)
special_palettes[1292] = define_palette(256, 6887000, sprites_file)
special_palettes[1679] = define_palette(256, subpaleta[385][0], subpaleta_file)
special_palettes[1680] = define_palette(256, subpaleta[385][0], subpaleta_file)


print('Started (Iniciado)')
timer = perf_counter()

for section in sections:
    offset = section[0]
    name = section[1]
    if not os.path.exists(f'extracted/graph/{name}/sprites'):
        os.makedirs(f'extracted/graph/{name}/sprites')
    
    images_count = int.from_bytes(file[offset+4:offset+8], 'little')
    sprites_count = int.from_bytes(file[offset+12:offset+16], 'little')
    sprites_size = int.from_bytes(file[offset+16:offset+20], 'little')
    header_size = 20
    
    offset += 20
    for x in range(images_count):
        width = int.from_bytes(file[offset:offset+4], 'little') * int.from_bytes(file[offset+8:offset+12], 'little')
        height = int.from_bytes(file[offset+4:offset+8], 'little') * int.from_bytes(file[offset+12:offset+16], 'little')
        offset += 20
        read_image(offset, width, height, f'{name}/{str(x).zfill(2)}')
        offset += width * height * 2

    print(offset)

    header = sprites_count * 20
    sprites = file[offset:offset+header+sprites_size]

    print('Extracting Sprites')
    sprites_offset = 0
    palette = []
    current_palette = None
    for n in range(sprites_count):
        image_offset = int.from_bytes(sprites[sprites_offset:sprites_offset+4], 'little') + header
        palette_offset = int.from_bytes(sprites[sprites_offset+4:sprites_offset+8], 'little') + header
        width = int.from_bytes(sprites[sprites_offset+8:sprites_offset+12], 'little')
        height = int.from_bytes(sprites[sprites_offset+12:sprites_offset+16], 'little')
        cores = int.from_bytes(sprites[sprites_offset+16:sprites_offset+20], 'little')

        if (n in special_palettes) and (special_palettes[n] != None):
            palette = special_palettes[n]

        elif palette_offset != current_palette:
            palette = define_palette(256, palette_offset, sprites)
            current_palette = palette_offset

        read_sprite(image_offset, width, height, palette, f'{name}/sprites/{str(n).zfill(4)}', sprites)

        sprites_offset += 20

print(perf_counter() - timer)
print('Finished (Terminado)')
