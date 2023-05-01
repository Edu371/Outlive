# by: Edu371
# Cria Vídeo PAF
# Creates PAF Video

import numpy as np
from PIL import Image
from time import perf_counter
from os import listdir
from os.path import isfile
import os
from numba import njit, prange, uint8, uint16
from math import ceil

images = {}
# path = 'frames'
path = input('Pasta(Path): ')
mode = input('1-Menu, Any-Cutscene: ')
width = int(input('Largura/Width (Max: 640, Divisible by 4)'))
height = int(input('Altura/Height (Max: 300, Divisible by 4)'))
output_name = input('Saída(Output): ')
if '.paf' not in output_name:
    output_name += '.paf'

files = [f for f in listdir(path) if isfile(f'{path}/{f}')]
for a in files:
    if '.png' in a:
        images[a.replace('.png', '')] = f'{path}/{a}'

if os.path.exists(f'{path}/audio.wav'):
    with open(f'{path}/audio.wav', 'rb') as audio_file:
        audio = audio_file.read()[44:]
    has_audio = 1
else:
    has_audio = 0
    audio = b''

if mode == '1':
    has_audio = 0
    unknown1 = 200000
    tipo = 65535
else:
    unknown1 = 600000
    tipo = 8

# utilize no minimo 45 frames (Use at least 45 frames)
frame_count = len(images)
# frame_count = 300
# width = 640
# height = 300
image_pixels = width * height
fps = 15 # Mais de 15 pode Causar Erros (More than 15 may cause Errors)
# unknown1= 600000 # 600000=cutscene; 200000=menu
color_paletes = ceil(frame_count / fps)
slices = frame_count + color_paletes + ceil(frame_count / fps) * has_audio
size = (12296 * color_paletes) + (ceil(frame_count / fps) * 44112) + (((width * height * 1.5) + (width * height / 32) + 14) * frame_count)
size += (ceil(frame_count / fps) * fps - frame_count) * 12
var = image_pixels * frame_count
if var < 192000000:
    unknown2 = var * 0.0125 + 50000 - 0.00022*var**1.2
else:
    unknown2 = 534050
unknown3= unknown2 * 12.5 # desconhecido
# tipo = 8 # 8 = cutscene; 65535 = menu(sem som)
if has_audio:
    audio_size = 44100
    bit_audio = 2
else:
    audio_size = 0
    bit_audio = 0

magic = b'PAF 2.0\x1a'
frame_count_bytes = int(frame_count).to_bytes(4, 'little')
width_bytes = int(width).to_bytes(4, 'little')
height_bytes = int(height).to_bytes(4, 'little')
fps_bytes = int(fps).to_bytes(4, 'little')
unknown1_bytes = int(unknown1).to_bytes(4, 'little')
has_audio_bytes = int(has_audio).to_bytes(4, 'little')
bit_audio_bytes = int(bit_audio).to_bytes(4, 'little')
slices_bytes = int(slices).to_bytes(4, 'little')
size_bytes = int(size).to_bytes(4, 'little')
unknown2_bytes = int(unknown2).to_bytes(4, 'little')
unknown3_bytes = int(unknown3).to_bytes(4, 'little')
tipo_bytes = int(tipo).to_bytes(4, 'little')
audio_size_bytes = int(audio_size).to_bytes(4, 'little')

data = b''
data += magic
data += frame_count_bytes
data += width_bytes
data += height_bytes
data += fps_bytes
data += unknown1_bytes
data += has_audio_bytes
data += bit_audio_bytes
data += slices_bytes
data += size_bytes
data += unknown2_bytes
data += unknown3_bytes
data += tipo_bytes
data += audio_size_bytes
data += b'\x00' * 68

colors = 256

def create_palette(palettes, offset):
    global data
    palette_data = b'\x01\x00\x00\x00\x00\x30\x00\x00'
    for x in palettes:
        palette_data += int(x).to_bytes(1, 'little')

    if len(palette_data) < 12296:
        for _ in range(12296-len(palette_data)):
            palette_data += int(0).to_bytes(1, 'little')

    data = data[:offset] + palette_data + data[offset:]

def convert_image(image, index):
    global data, buffer_frame
    if image == 'empty':
        data += b'\x04\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00'
        return
    image_data = b'\x04\x00\x00\x00'
    image_size = int(image_pixels * 1.5)
    copy_size = int(image_pixels / 32)
    copy_index = None

    copy = np.full(copy_size * 2, 14, dtype=int)

    sections =  np.asarray(image).reshape(height//4, 4, -1, 2
                                  ).swapaxes(1,2).reshape(-1, 2, 2, 4
                                  ).swapaxes(1, 2).reshape(-1, 16)

    buffer_frame2 = sections.copy()
    
    if buffer_frame is not None:
        copy_index = np.where((buffer_frame == sections).all(axis=1))
        copy[copy_index] = 0
        sections = np.delete(sections, copy_index, 0)
    
    ##### Coisa de Maluco (Crazy Man Stuff)
    
    copy_index2 = np.where((buffer_frame2 == buffer_frame2[:, 0, None]).all(1))[0]
    if copy_index is not None:
        copy_index2 = np.delete(copy_index2, np.intersect1d(copy_index, copy_index2, return_indices=True)[2])

    copy[copy_index2] = 1
    
    copy_index = np.where((sections == sections[:, 0, None]).all(1))[0]
    n = sections[:, 0][copy_index]
    sections = np.delete(sections, copy_index, 0)

    insert_index = (copy_index - np.arange(copy_index.size)) * 16

    sections = np.insert(sections, insert_index, n)

    if sections.size % 16 != 0:
        sections = np.append(sections, [0] * (16 - (sections.size % 16)))

    sections = sections.reshape(-1, 16)
    
    #####

    copy = np.sum(copy.reshape(-1, 2) * np.array([1, 16], dtype=int), axis=1)
    buffer_frame = buffer_frame2.copy()

    image_data += int(sections.size * 1.5 + copy_size + 6).to_bytes(4, 'little')
    image_data += int(copy_size + 6).to_bytes(4, 'little')

    image_data += bytes(copy.tolist())

    image_data += int(0).to_bytes(2, 'little')

    image_data += bytes(convert_numba(sections))

    data += image_data

@njit(fastmath=True)
def binary(number, size_of_bin = 12):
    out = np.zeros(size_of_bin, uint8)
    num = number
    index = 11

    for i in prange(size_of_bin):
        floatDivide = num // 2
        divide = num / 2
        if floatDivide != divide:
            out[index] = 1
    
        num = floatDivide
        
        index-= 1
        if index == -1 or floatDivide == 0:
            break

    return out

@njit(locals = {'y': uint16})
def to_int(x):
    y = 0
    for i,j in enumerate(x[::-1]):
        y += j<<i
    return y

@njit
def convert_numba(sections):
    image_data = []
    
    # print(section)
    for x in sections:
        # print(x)
        pixel0 = binary(x[0])
        pixel1 = binary(x[1])
        pixel2 = binary(x[2])
        pixel3 = binary(x[3])
        pixel4 = binary(x[4])
        pixel5 = binary(x[5])
        pixel6 = binary(x[6])
        pixel7 = binary(x[7])
        pixel8 = binary(x[8])
        pixel9 = binary(x[9])
        pixel10 = binary(x[10])
        pixel11 = binary(x[11])
        pixel12 = binary(x[12])
        pixel13 = binary(x[13])
        pixel14 = binary(x[14])
        pixel15 = binary(x[15])

        byte0 = to_int(pixel0[4:])
        byte1 = to_int(np.concatenate((pixel1[8:], pixel0[:4])))
        byte2 = to_int(pixel1[:8])
        
        byte4 = to_int(pixel2[4:])
        byte5 = to_int(np.concatenate((pixel3[8:], pixel2[:4])))
        byte6 = to_int(pixel3[:8])
        
        byte8 = to_int(pixel4[4:])
        byte9 = to_int(np.concatenate((pixel5[8:], pixel4[:4])))
        byte10 = to_int(pixel5[:8])

        byte11 = to_int(pixel6[4:])
        byte7 = to_int(np.concatenate((pixel7[8:], pixel6[:4])))
        byte3 = to_int(pixel7[:8])

        byte12 = to_int(pixel8[4:])
        byte13 = to_int(np.concatenate((pixel9[8:], pixel8[:4])))
        byte14 = to_int(pixel9[:8])
        
        byte16 = to_int(pixel10[4:])
        byte17 = to_int(np.concatenate((pixel11[8:], pixel10[:4])))
        byte18 = to_int(pixel11[:8])
        
        byte20 = to_int(pixel12[4:])
        byte21 = to_int(np.concatenate((pixel13[8:], pixel12[:4])))
        byte22 = to_int(pixel13[:8])

        byte23 = to_int(pixel14[4:])
        byte19 = to_int(np.concatenate((pixel15[8:], pixel14[:4])))
        byte15 = to_int(pixel15[:8])

        image_data.append(byte0)
        image_data.append(byte1)
        image_data.append(byte2)
        image_data.append(byte3)
        image_data.append(byte4)
        image_data.append(byte5)
        image_data.append(byte6)
        image_data.append(byte7)
        image_data.append(byte8)
        image_data.append(byte9)
        image_data.append(byte10)
        image_data.append(byte11)

        image_data.append(byte12)
        image_data.append(byte13)
        image_data.append(byte14)
        image_data.append(byte15)
        image_data.append(byte16)
        image_data.append(byte17)
        image_data.append(byte18)
        image_data.append(byte19)
        image_data.append(byte20)
        image_data.append(byte21)
        image_data.append(byte22)
        image_data.append(byte23)
                          

    return image_data

def add_audio(index):
    global data
    audio_data = b'\x02\x00\x00\x00\x48\xAC\x00\x00\x00\x00\x00\x00'
    audio_data += audio[index*audio_size: index*audio_size+audio_size]
    if len(audio_data) < audio_size+12:
        for _ in range(audio_size+12-len(audio_data)):
            audio_data += int(0).to_bytes(1, 'little')
    data += audio_data

def convert_palette(img, palette, img_palette):
    buffer = np.zeros(len(img), dtype=int)
    img = np.asarray(img)
    for x in range(len(img_palette)):
        buffer[np.where(img == x)] = palette.index(img_palette[x])
    
    buffer = buffer.tolist()
    return buffer

def palette2chunks(p):
    for i in range(0, len(p), 3):
        yield p[i:i + 3]

def flatten(l):
    return [item for sublist in l for item in sublist]

def add2list(l1, l2):
    for i in l2:
        if i not in l1:
            l1.append(i)

def add_array(a, b):
    A = np.array(a)
    B = np.array(b)

    nrows, ncols = A.shape
    dtype={'names':['f{}'.format(i) for i in range(ncols)],
       'formats':ncols * [A.dtype]}

    c = np.intersect1d(A.view(dtype), B.view(dtype), return_indices=True, assume_unique=True)[2]

    B = np.delete(B, c, 0).tolist()

    a.extend(B)

timer = perf_counter()
color_paletes = 0

buffer_frame = None

current_palette = []
palette_offset = 128
for n in range(0, frame_count, fps):
    frames = []
    palette = [[0, 0, 0]]
    palette_change = False
    for i in range(n, n+fps):
        if i < frame_count:
            image = Image.open(images[str(i).zfill(4)]).quantize(colors)
            
            img_palette = list(palette2chunks(list(image.getpalette())[:colors*3]))
            # add2list(palette, img_palette)
            if not palette:
                # palette = img_palette.copy()
                add2list(palette, img_palette)
                
            else:
                add_array(palette, img_palette)

            frames.append((list(image.getdata()), img_palette))

        else:
            frames.append('empty')
    
    if current_palette:
        buffer_palette = []
        
        # add2list(buffer_palette, current_palette)
        buffer_palette = current_palette.copy()
        # add2list(buffer_palette, palette)
        add_array(buffer_palette, palette)
        
        if len(buffer_palette) <= 4096:
            current_palette = buffer_palette.copy()
            print('Paleta Mantida (Palette Keeped)')

        else:
            create_palette(flatten(current_palette), palette_offset)
            print(palette_offset, len(flatten(current_palette)))
            color_paletes += 1
            current_palette = palette.copy()
            palette_offset = len(data)
            palette_change = True

    else:
        current_palette = palette.copy()

    for i in range(len(frames)):
        if frames[i] != 'empty':
            img = convert_palette(frames[i][0], current_palette, frames[i][1])
            frames[i] = img

    if has_audio:
        add_audio(int(n/fps))
    
    for index, image in enumerate(frames):
        convert_image(image, index)
    if palette_change:
        buffer_frame = None

    if n+fps >= frame_count:
        create_palette(flatten(current_palette), palette_offset)
        color_paletes += 1
        print('Final Palette')
    
    print(f'Converted {int(n/fps)+1}s')
    print(perf_counter() - timer)

slices = frame_count + color_paletes + ceil(frame_count / fps) * has_audio
size = len(data) - 128
slices_bytes = int(slices).to_bytes(4, 'little')
size_bytes = int(size).to_bytes(4, 'little')
data = data[:36] + slices_bytes + size_bytes + data[44:]

with open(output_name, 'wb') as outfile:
    outfile.write(data)

    
print(perf_counter() - timer)
