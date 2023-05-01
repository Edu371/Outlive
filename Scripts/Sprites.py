# by: Edu371
# Extrai Sprites
# Extracts Sprites

from PIL import Image
import numpy as np
import os


file_name = 'Outlive.dat'

file = open(file_name, 'rb')
file = file.read()

sprites = file[4108:12481239]

subpaleta_file = file[12481239:13197983]

infotipo_file = file[113622304:113971525]

if not os.path.exists('extracted/sprites'):
    os.makedirs('extracted/sprites')

for x in range(17):
    if not os.path.exists(f'extracted/sprites/alternative_{str(x).zfill(2)}'):
        os.makedirs(f'extracted/sprites/alternative_{str(x).zfill(2)}')

subpaleta = {}
subpaleta_count = int.from_bytes(subpaleta_file[0:4], 'little')
for var in range(subpaleta_count):
    offset = int.from_bytes(subpaleta_file[8+var*16:12+var*16], 'little') + 968
    palette_id = int.from_bytes(subpaleta_file[12+var*16:16+var*16], 'little')
    variations = int.from_bytes(subpaleta_file[16+var*16:20+var*16], 'little')
    colors = int.from_bytes(subpaleta_file[20+var*16:24+var*16], 'little') * 256
    subpaleta[palette_id] = [offset, variations, colors]


infotipo = []
infotipo_count = int.from_bytes(infotipo_file[0:4], 'little')
for var in range(infotipo_count):
    infotipo_id = int.from_bytes(infotipo_file[4+var*911:8+var*911], 'little')
    if (infotipo_file[756+var*911:758+var*911] == b'\x00\x00'
        ) or (infotipo_file[756+var*911:758+var*911] == b'\xFF\xFF'):
        # type = 'unit'
        initial_sprite = int.from_bytes(infotipo_file[18+var*911:20+var*911], 'little')
    else:
        # type = 'building'
        initial_sprite = int.from_bytes(infotipo_file[756+var*911:758+var*911], 'little')

    name = str(infotipo_file[507+var*911:531+var*911], 'iso-8859-1').replace('\x00', '')
    if initial_sprite:
        infotipo.append([infotipo_id, initial_sprite, name])
    

infotipo = sorted(infotipo, key=lambda e: e[1])
# infotipo = [[infotipo_id, initial_sprite, name, final_sprite]...]

var = 0
for _ in range(len(infotipo)-1):
    if infotipo[var][1] != infotipo[var+1][1]:
        infotipo[var].append(infotipo[var+1][1])
        var += 1
    else:
        del infotipo[var+1]


image_count = int.from_bytes(sprites[12:16], 'little')
header = 20 + image_count * 20
n = 0

infotipo[-1].append(image_count)

offset = 20
palette = []
alt_palettes = []
current_palette = None
current_index = None

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

def process_image(image_offset, width, height, palette, name):
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
    image.save(f'extracted/sprites/{name}.png')
    print(f'saved {name}.png')

print('Started (Iniciado)')

infotipo_id = None
for _ in range(image_count):
    image_offset = int.from_bytes(sprites[offset:offset+4], 'little') + header
    palette_offset = int.from_bytes(sprites[offset+4:offset+8], 'little') + header
    width = int.from_bytes(sprites[offset+8:offset+12], 'little')
    height = int.from_bytes(sprites[offset+12:offset+16], 'little')
    cores = int.from_bytes(sprites[offset+16:offset+20], 'little') * 256
    if current_index is None:
        if n >= infotipo[0][1]:
            current_index = 0
            infotipo_id = infotipo[current_index][0]
    else:
        if infotipo[current_index][3] <= n:
            current_index += 1

        infotipo_id = infotipo[current_index][0]

    if infotipo_id in subpaleta:
        if current_palette != infotipo_id:
            palette_offset = subpaleta[infotipo_id][0]
            alternatives = subpaleta[infotipo_id][1]
            cores = subpaleta[infotipo_id][2]
            palette = define_palette(cores, palette_offset, subpaleta_file)
            alt_palettes = []
            for x in range(1, alternatives):
                alt_palettes.append(define_palette(cores, palette_offset+(cores * 2 * x), subpaleta_file))
                            
            current_palette = infotipo_id
            
            
    elif palette_offset != current_palette:
        palette = define_palette(cores, palette_offset, sprites)
        alternatives = 0
        current_palette = palette_offset

    process_image(image_offset, width, height, palette, str(n).zfill(5))
    for x in range(alternatives-1):
        process_image(image_offset, width, height, alt_palettes[x], f'alternative_{str(x).zfill(2)}/{str(n).zfill(5)}')

    n += 1
    offset += 20

print('Finished (Terminado)')
