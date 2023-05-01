import numpy as np
from PIL import Image
import os

file_name = 'Outlive.dat'

file = open(file_name, 'rb')
file = file.read()

sections = [[162536142, 'TERRAIN_FOREST'],
            [165365366, 'TERRAIN_URBAN']]

colors = 256
palette = []

if not os.path.exists('extracted/terrain'):
    os.makedirs('extracted/terrain')

def read_palette(palette_offset):
    print('Lendo Paleta (Reading Palette)')
    global palette
    palette = []
    for var in range(colors):
        color = file[palette_offset + var * 3: palette_offset + var * 3 + 3]
        color = [int(color[0]), int(color[1]), int(color[2])]
        palette.append(color)

def read_image(image_offset, width, height, name):
    size = width * height
    data = file[image_offset:image_offset + size]
    image = []
    for c in range(size):
        image.append(palette[data[c]])
    i = np.asarray(image).reshape((height, width, 3)).astype(np.uint8)
    image = Image.fromarray(i)
    image.save(f'extracted/terrain/{name}.png')

print('Started (Iniciado)')

for section in sections:
    offset = section[0]
    if not os.path.exists(f'extracted/terrain/{section[1]}'):
        os.makedirs(f'extracted/terrain/{section[1]}')
    n = int.from_bytes(file[offset:offset+4], 'little')
    n_obj = int.from_bytes(file[offset+4:offset+8], 'little')
    header = n * 16 + 12
    header_full = header + n_obj * 768
    offset += 12
    current_object = None
    for x in range(n):
        image_offset = int.from_bytes(file[offset:offset+4], 'little')
        object_id = int.from_bytes(file[offset+4:offset+8], 'little')
        if object_id != current_object:
            read_palette(section[0] + header + object_id * 768)
            current_object = object_id
        read_image(section[0] + header_full + image_offset, 48, 24, f'{section[1]}/{str(x).zfill(4)}')
        offset += 16

print('Finished (Terminado)')
