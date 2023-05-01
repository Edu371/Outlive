# by: Edu371
# Extrai Vídeo PAF
# Extracts PAF Video

import numpy as np
from PIL import Image
from Vizualizer import Player
import os
import time

timer = time.perf_counter()

# file_name = 'Menu01.paf'
file_name = input('Arquivo(File): ')
if '.paf' not in file_name:
    file_name += '.paf'

file = open(file_name, 'rb')
file = file.read()

header = 128
offset = header
cores = 4096
frames = []
legenda = {}
audio = b''
frames_saved = 0

# player or extractor
mode = input('Mode: 1-Player, Any-Extractor: ')
if mode == '1':
    mode = 'player'
else:
    mode = 'extractor'

if mode == 'extractor':
    if not os.path.exists(f'extracted/pafs/{file_name[:-4]}'):
        os.makedirs(f'extracted/pafs/{file_name[:-4]}')

# Lendo Header
frame_count = int.from_bytes(file[8:12], 'little')
width = int.from_bytes(file[12:16], 'little')
height = int.from_bytes(file[16:20], 'little')
fps = int.from_bytes(file[20:24], 'little')
unknown = int.from_bytes(file[24:28], 'little')  # 600000 = cutscene; 200000 = menu
has_audio = bool(int.from_bytes(file[28:32], 'little'))
bit_audio = int.from_bytes(file[32:36], 'little') * 8
slices = int.from_bytes(file[36:40], 'little')  # sem utilidade
size = int.from_bytes(file[40:44], 'little') + header
unknown2 = int.from_bytes(file[48:52], 'little')  # desconhecido
tipo = int.from_bytes(file[52:56], 'little')  # 8 = cutscene; 65535 = menu
audio_size = int.from_bytes(file[56:60], 'little')  # padrão = 44100

image_size = int(width * height * 1.5)
image_pixels = width * height


def read_palete(palete_offset):
    print('Lendo Paleta (Reading Palette)')
    global color_table
    color_table = []
    for var in range(cores):
        color = file[palete_offset + var * 3: palete_offset + var * 3 + 3]
        color = [int(color[0]), int(color[1]), int(color[2]), 255]
        color_table.append(color)


def read_audio(audio_offset):
    print('Lendo Áudio (Reading Audio)')
    global audio
    audio += file[audio_offset: audio_offset + audio_size]


def read_frame(frame_offset):
    print('Lendo Frame (Reading Frame)')
    frame_size = int.from_bytes(file[frame_offset:frame_offset + 4], 'little') + 8
    header_size = int.from_bytes(file[frame_offset + 4:frame_offset + 8], 'little') + 4
    real_size = frame_size - header_size - 4
    if real_size == 4:
        i = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        frames.append(i)
        return 12
    copy_index = []
    for x in range(header_size - 8):
        copy_index.append(int(bin(file[frame_offset + x + 8])[2:].zfill(8)[4:], 2))
        copy_index.append(int(bin(file[frame_offset + x + 8])[2:].zfill(8)[:4], 2))

    sections = []
    frame = file[frame_offset + header_size:frame_offset + header_size + real_size]
    for x in range(0, real_size, 24):
        section = frame[x: x + 24]

        byte0 = section[0]
        byte1 = section[1]
        byte2 = section[2]
        byte3 = section[3]
        byte4 = section[4]
        byte5 = section[5]
        byte6 = section[6]
        byte7 = section[7]
        byte8 = section[8]
        byte9 = section[9]
        byte10 = section[10]
        byte11 = section[11]

        pixel0 = int(bin(byte1)[2:].zfill(8)[4:] + bin(byte0)[2:].zfill(8), 2)
        pixel1 = int(bin(byte2)[2:].zfill(8) + bin(byte1)[2:].zfill(8)[:4], 2)

        pixel2 = int(bin(byte5)[2:].zfill(8)[4:] + bin(byte4)[2:].zfill(8), 2)
        pixel3 = int(bin(byte6)[2:].zfill(8) + bin(byte5)[2:].zfill(8)[:4], 2)

        pixel4 = int(bin(byte9)[2:].zfill(8)[4:] + bin(byte8)[2:].zfill(8), 2)
        pixel5 = int(bin(byte10)[2:].zfill(8) + bin(byte9)[2:].zfill(8)[:4], 2)

        pixel6 = int(bin(byte7)[2:].zfill(8)[4:] + bin(byte11)[2:].zfill(8), 2)
        pixel7 = int(bin(byte3)[2:].zfill(8) + bin(byte7)[2:].zfill(8)[:4], 2)

        pixel0 = color_table[pixel0]
        pixel1 = color_table[pixel1]
        pixel2 = color_table[pixel2]
        pixel3 = color_table[pixel3]
        pixel4 = color_table[pixel4]
        pixel5 = color_table[pixel5]
        pixel6 = color_table[pixel6]
        pixel7 = color_table[pixel7]

        if len(section) == 24:
            byte12 = section[12]
            byte13 = section[13]
            byte14 = section[14]
            byte15 = section[15]
            byte16 = section[16]
            byte17 = section[17]
            byte18 = section[18]
            byte19 = section[19]
            byte20 = section[20]
            byte21 = section[21]
            byte22 = section[22]
            byte23 = section[23]

            pixel8 = int(bin(byte13)[2:].zfill(8)[4:] + bin(byte12)[2:].zfill(8), 2)
            pixel9 = int(bin(byte14)[2:].zfill(8) + bin(byte13)[2:].zfill(8)[:4], 2)

            pixel10 = int(bin(byte17)[2:].zfill(8)[4:] + bin(byte16)[2:].zfill(8), 2)
            pixel11 = int(bin(byte18)[2:].zfill(8) + bin(byte17)[2:].zfill(8)[:4], 2)

            pixel12 = int(bin(byte21)[2:].zfill(8)[4:] + bin(byte20)[2:].zfill(8), 2)
            pixel13 = int(bin(byte22)[2:].zfill(8) + bin(byte21)[2:].zfill(8)[:4], 2)

            pixel14 = int(bin(byte19)[2:].zfill(8)[4:] + bin(byte23)[2:].zfill(8), 2)
            pixel15 = int(bin(byte15)[2:].zfill(8) + bin(byte19)[2:].zfill(8)[:4], 2)

            pixel8 = color_table[pixel8]
            pixel9 = color_table[pixel9]
            pixel10 = color_table[pixel10]
            pixel11 = color_table[pixel11]
            pixel12 = color_table[pixel12]
            pixel13 = color_table[pixel13]
            pixel14 = color_table[pixel14]
            pixel15 = color_table[pixel15]

            sections.extend([pixel0, pixel1, pixel2, pixel3, pixel4, pixel5, pixel6, pixel7,
                             pixel8, pixel9, pixel10, pixel11, pixel12, pixel13, pixel14, pixel15])
        else:
            sections.extend([pixel0, pixel1, pixel2, pixel3, pixel4, pixel5, pixel6, pixel7])

    current_copy_index = 0
    current_section = 0
    for _ in range(len(copy_index)):
        current_copy = copy_index[current_copy_index]

        if current_copy == 0:
            buffer = [[0, 0, 0, 0] for _ in range(16)]
            sections[current_section:current_section] = buffer

        elif current_copy == 1:
            sections[current_section:current_section] = sections[current_section:current_section + 1] * 15

        elif current_copy == 2:
            sections[current_section:current_section] = sections[current_section:current_section + 1] * 3
            sections[current_section + 4:current_section + 4] = sections[current_section + 4:current_section + 5] * 3
            sections[current_section + 8:current_section + 8] = sections[current_section + 8:current_section + 9] * 3
            sections[current_section + 12:current_section + 12] = sections[
                                                                  current_section + 12:current_section + 13] * 3

        elif current_copy == 3:
            sections[current_section:current_section] = sections[current_section:current_section + 1] * 3
            sections[current_section + 4:current_section + 4] = sections[current_section + 4:current_section + 5] * 3
            sections[current_section + 8:current_section + 8] = sections[current_section + 8:current_section + 9] * 7

        elif current_copy == 4:
            sections[current_section:current_section] = sections[current_section:current_section + 1] * 3
            sections[current_section + 4:current_section + 4] = sections[current_section + 4:current_section + 5] * 3
            sections[current_section + 8:current_section + 8] = sections[current_section:current_section + 1] * 4
            sections[current_section + 12:current_section + 12] = sections[
                                                                  current_section + 12:current_section + 13] * 3

        elif current_copy == 5:
            sections[current_section:current_section] = sections[current_section:current_section + 1] * 7
            sections[current_section + 8:current_section + 8] = sections[current_section + 8:current_section + 9] * 3
            sections[current_section + 12:current_section + 12] = sections[
                                                                  current_section + 12:current_section + 13] * 3

        elif current_copy == 6:
            sections[current_section + 4:current_section + 4] = sections[current_section + 4:current_section + 5] * 3
            sections[current_section + 8:current_section + 8] = sections[current_section + 8:current_section + 9] * 3
            sections[current_section + 12:current_section + 12] = sections[
                                                                  current_section + 12:current_section + 13] * 3

        elif current_copy == 7:
            sections[current_section:current_section] = sections[current_section:current_section + 1] * 3
            sections[current_section + 8:current_section + 8] = sections[current_section + 8:current_section + 9] * 3
            sections[current_section + 12:current_section + 12] = sections[
                                                                  current_section + 12:current_section + 13] * 3

        elif current_copy == 8:
            sections[current_section:current_section] = sections[current_section:current_section + 1] * 3
            sections[current_section + 4:current_section + 4] = sections[current_section + 4:current_section + 5] * 3
            sections[current_section + 8:current_section + 8] = sections[current_section + 8:current_section + 9] * 3

        elif current_copy == 9:
            sections[current_section:current_section] = sections[current_section:current_section + 1] * 3
            sections[current_section + 4:current_section + 4] = sections[current_section + 4:current_section + 5] * 3
            sections[current_section + 12:current_section + 12] = sections[
                                                                  current_section + 12:current_section + 13] * 3

        elif current_copy == 10:
            sections[current_section:current_section] = sections[current_section:current_section + 1] * 3
            sections[current_section + 4:current_section + 4] = sections[current_section + 4:current_section + 5] * 3

        elif current_copy == 11:
            sections[current_section + 4:current_section + 4] = sections[current_section + 4:current_section + 5] * 3
            sections[current_section + 12:current_section + 12] = sections[
                                                                 current_section + 12:current_section + 13] * 3

        elif current_copy == 12:
            sections[current_section + 8:current_section + 8] = sections[current_section + 8:current_section + 9] * 3
            sections[current_section + 12:current_section + 12] = sections[
                                                                 current_section + 12:current_section + 13] * 3

        elif current_copy == 13:
            sections[current_section:current_section] = sections[current_section:current_section + 1] * 3
            sections[current_section + 8:current_section + 8] = sections[current_section + 8:current_section + 9] * 3

        elif current_copy == 14:
            pass

        elif current_copy == 15:
            multiplier = copy_index[current_copy_index + 1] - 14
            buffer = [[0, 0, 0, 0] for _ in range(272 + multiplier * 16)]
            sections[current_section:current_section] = buffer
            current_copy_index += 1
            current_section += (256 + multiplier * 16)

        current_copy_index += 1
        current_section += 16

        if current_copy_index >= len(copy_index):
            break

    if len(sections) < image_pixels:
        print('####################Bytes Insuficientes####################')
        print('Adicionado:', int(image_pixels - len(sections)))
        for _ in range(int(image_pixels - len(sections))):
            sections.append([0, 0, 0, 0])

    # Separar Sections
    for var in range(len(sections) // 16):
        sections[var:var + 16] = [sections[var:var + 16]]

    image = []
    row_size = int(image_pixels / 16 / (height / 4))
    for row in range(0, int(height / 4)):
        line0 = []
        line1 = []
        line2 = []
        line3 = []
        section = sections[row * row_size: row * row_size + row_size]
        for x in range(0, row_size, 1):
            line0.extend(section[x][:2])
            line0.extend(section[x][4:6])
            line1.extend(section[x][2:4])
            line1.extend(section[x][6:8])
            line2.extend(section[x][8:10])
            line2.extend(section[x][12:14])
            line3.extend(section[x][10:12])
            line3.extend(section[x][14:])

        image.extend(line0)
        image.extend(line1)
        image.extend(line2)
        image.extend(line3)

    i = np.asarray(image[:image_pixels]).reshape((height, width, 4)).astype(np.uint8)
    frames.append(Image.fromarray(i))
    return frame_size


def read_legenda(legenda_offset):
    print('Lendo Legenda (Reading Subtitles)')
    leg1_size = int.from_bytes(file[legenda_offset:legenda_offset + 4], 'little')
    leg2_size = int.from_bytes(file[legenda_offset + leg1_size + 8:legenda_offset + leg1_size + 12], 'little')

    final_frame = int.from_bytes(file[legenda_offset + 8:legenda_offset + 12], 'little')
    if mode == 'extractor':
        l_index = frames_saved
    else:
        l_index = len(frames)

    legenda[l_index] = [final_frame, str(file[legenda_offset + 12: legenda_offset + leg1_size + 4], 'iso-8859-1'),
                                        str(file[
                                            legenda_offset + leg1_size + 20: legenda_offset + leg1_size + leg2_size + 12],
                                            'iso-8859-1')]

    return leg1_size + leg2_size + 16

print('Started (Iniciado)')

while offset < size:
    identifier = file[offset: offset + 8]
    if identifier == b'\x01\x00\x00\x00\x00\x30\x00\x00':
        read_palete(offset + 8)
        offset += cores * 3 + 8
    elif identifier == b'\x02\x00\x00\x00\x48\xAC\x00\x00':
        read_audio(offset + 12)
        offset += audio_size + 12
    elif identifier[:4] == b'\x03\x00\x00\x00':
        offset += read_legenda(offset + 4)
        print(offset)
    elif identifier[:4] == b'\x04\x00\x00\x00':
        image_offset = read_frame(offset + 4)
        offset += image_offset
        print(offset)
        if mode == 'extractor':
            if len(frames) > 1:
                frames[-1] = Image.alpha_composite(frames[0], frames[-1])
                frames[-1].save(f'extracted/pafs/{file_name[:-4]}/{str(frames_saved).zfill(4)}.png')
                frames_saved += 1
                del frames[0]

            elif len(frames) == 1:
                frames[-1].save(f'extracted/pafs/{file_name[:-4]}/{str(frames_saved).zfill(4)}.png')
                frames_saved += 1
            print(f'{str(frames_saved - 1).zfill(4)}.png')
    else:
        print('travado')
        break

if mode == 'extractor':
    if audio:
        with open(f'extracted/pafs/{file_name[:-4]}/audio.wav', 'wb') as outfile:
            outfile.write(b'RIFF')
            outfile.write(int(len(audio) + 36).to_bytes(4, 'little'))
            outfile.write(b'WAVEfmt\x20')
            outfile.write(b'\x10\x00\x00\x00')
            outfile.write(b'\x01\x00\x01\x00')
            outfile.write(b'\x22\x56\x00\x00')
            outfile.write(b'\x44\xAC\x00\x00')
            outfile.write(b'\x02\x00\x10\x00')
            outfile.write(b'data')
            outfile.write(int(len(audio)).to_bytes(4, 'little'))
            outfile.write(audio)

    if legenda:
        with open(f'extracted/pafs/{file_name[:-4]}/legenda.txt', 'wb') as outfile:
            for n, x in enumerate(legenda):
                outfile.write(bytes(f'{n + 1}\n','iso_8859-1'))
                outfile.write(bytes(f'{str(int(x) // fps // 3600).zfill(2)}:{str(int(x) // fps % 3600 // 60).zfill(2)}:{f"{int(x) / fps % 60:0.3f}".zfill(6)}',
                                    'iso_8859-1'))
                outfile.write(bytes(f' --> {str(legenda[x][0] // fps // 3600).zfill(2)}:{str(legenda[x][0] // fps % 3600 // 60).zfill(2)}:{f"{legenda[x][0] / fps % 60:0.3f}".zfill(6)}\n',
                                    'iso_8859-1'))
                outfile.write(bytes(f'Português: {str(legenda[x][1])}\n', 'iso_8859-1'))
                outfile.write(bytes(f'English: {legenda[x][2]}\n', 'iso_8859-1'))
                outfile.write(bytes(f'\n', 'iso_8859-1'))

print('Finished (Terminado)')
print(time.perf_counter() - timer)
if mode == 'player':
    Player(frames, audio, fps, [width, height], legenda, False, alpha=True)
