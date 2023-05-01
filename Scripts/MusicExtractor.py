# by: Edu371
# Extrai Musicas de music.dat
# Extracts Musics from music.dat

import os

file_name = 'music.dat'

file = open(file_name, 'rb')
file = file.read()

if not os.path.exists('extracted/music'):
    os.makedirs('extracted/music')

if file[:16] != b'\x01\x00\x00\x00[MUSIC]\x00\x00\x00\x00\x00':
    raise Exception('Arquivo Incorreto (Incorrect File)')

def save(name, offset, size):
    with open(f'extracted/music/{name}.wav', 'wb') as outfile:
        outfile.write(b'RIFF')
        outfile.write((size + 36).to_bytes(4, 'little'))
        outfile.write(b'WAVEfmt\x20')
        outfile.write(b'\x10\x00\x00\x00')
        outfile.write(b'\x01\x00\x02\x00')
        outfile.write(b'\x22\x56\x00\x00')
        outfile.write(b'\x88\x58\x01\x00')
        outfile.write(b'\x04\x00\x10\x00')
        outfile.write(b'data')
        outfile.write(size.to_bytes(4, 'little'))
        outfile.write(file[offset:offset+size])

n_musicas =  int.from_bytes(file[40:44], 'little')

header = 100

offset_1 = int.from_bytes(file[44:48], 'little') + header
size_1 = int.from_bytes(file[48:52], 'little')

offset_2 = int.from_bytes(file[52:56], 'little') + header
size_2 = int.from_bytes(file[56:60], 'little')

offset_3 = int.from_bytes(file[60:64], 'little') + header
size_3 = int.from_bytes(file[64:68], 'little')

offset_4 = int.from_bytes(file[68:72], 'little') + header
size_4 = int.from_bytes(file[72:76], 'little')

offset_5 = int.from_bytes(file[76:80], 'little') + header
size_5 = int.from_bytes(file[80:84], 'little')

offset_6 = int.from_bytes(file[84:88], 'little') + header
size_6 = int.from_bytes(file[88:92], 'little')

offset_7 = int.from_bytes(file[92:96], 'little') + header
size_7 = int.from_bytes(file[96:100], 'little')

print('Started (Iniciado)')

save('music01', offset_1, size_1)
save('music02', offset_2, size_2)
save('music03', offset_3, size_3)
save('music04', offset_4, size_4)
save('music05', offset_5, size_5)
save('music06', offset_6, size_6)
save('music07', offset_7, size_7)

print('Finished (Terminado)')
