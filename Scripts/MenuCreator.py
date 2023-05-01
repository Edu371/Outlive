# by: Edu371
# Insere Imagens em GRAPH_MENU
# Insert Images in GRAPH_MENU

import numpy as np
from PIL import Image
import os
from os import listdir
from os.path import isfile

# file_name = 'Outlive.dat'
file_name = input('Outlive.dat(Path): ')

file = open(file_name, 'rb')
file = file.read()

new_file = file
offset = 43644530
offset2 = 49926027
images_count = 8
images_count2 = 18
images = {}

path = input('Pasta(Path): ')
output_name = input('Saída(Output): ')
if '.dat' not in output_name:
    output_name += '.dat'

files = [f for f in listdir(path) if isfile(f'{path}/{f}')]
for a in files:
    if '.png' in a:
        images[a.replace('.png', '')] = f'{path}/{a}'

def convert_image(image_index, image_offset):
    global new_file
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

    new_file = new_file[:image_offset] + data + new_file[image_offset + size:]

print('Started (Iniciado)')
for x in range(images_count):
    if str(x).zfill(2) in images:
        print(f'Convertendo Image {str(x).zfill(2)}.png')
        width = int.from_bytes(file[offset:offset+4], 'little')
        height = int.from_bytes(file[offset+4:offset+8], 'little')
        width = width * int.from_bytes(file[offset+8:offset+12], 'little')
        height = height * int.from_bytes(file[offset+12:offset+16], 'little')
        size = width * height * 2
        convert_image(str(x).zfill(2), offset + 20)
    offset += size + 20

    print(offset)

offset = offset2
for x in range(images_count, images_count + images_count2):
    if str(x).zfill(2) in images:
        print(f'Convertendo Image {str(x).zfill(2)}.png')
        width = int.from_bytes(file[offset:offset+4], 'little')
        height = int.from_bytes(file[offset+4:offset+8], 'little')
        width = width * int.from_bytes(file[offset+8:offset+12], 'little')
        height = height * int.from_bytes(file[offset+12:offset+16], 'little')
        size = width * height * 2
        convert_image(str(x).zfill(2), offset + 20)
    offset += size + 40

    print(offset)

output = open(output_name, 'wb')
output.write(new_file)
output.close()
print('Finished (Terminado)')
