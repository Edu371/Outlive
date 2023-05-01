# by: Edu371
# Extrai Efeitos Sonoros
# Extracts Sound Effects

import os

file_name = 'Outlive.dat'

file = open(file_name, 'rb')
file = file.read()

file = file[13299861:43604505]

if not os.path.exists('extracted/sound'):
    os.makedirs('extracted/sound')

def save(name, offset, tamanho):
    with open(f'extracted/sound/{name}.wav', 'wb') as outfile:
        outfile.write(b'RIFF')
        outfile.write((tamanho + 36).to_bytes(4, 'little'))
        outfile.write(b'WAVEfmt\x20')
        outfile.write(b'\x10\x00\x00\x00')
        outfile.write(b'\x01\x00\x01\x00')
        outfile.write(b'\x22\x56\x00\x00')
        outfile.write(b'\x44\xAC\x00\x00')
        outfile.write(b'\x02\x00\x10\x00')
        outfile.write(b'data')
        outfile.write(tamanho.to_bytes(4, 'little'))
        outfile.write(file[offset:offset+tamanho])

n_sfx =  489

header = 17692
offset = 16
sound_list = []
negative = 157604

print('Started (Iniciado)')

for _ in range(n_sfx):
    sound_list.append([int.from_bytes(file[offset+12:offset+16], 'little'),
                       int.from_bytes(file[offset+24:offset+28], 'little') - negative])
    offset += 32

for n, x in enumerate(sound_list):
    save(str(n).zfill(3), x[1] + header, x[0])

print('Finished (Terminado)')
