# by: Edu371
# Insere Musicas em music.dat
# Insert Musics in music.dat

import os

path = input('Pasta(Path): ')
output_name = input('Saída(Output): ')
if '.dat' not in output_name:
    output_name += '.dat'

file = b'\x01\x00\x00\x00[MUSIC]\x00\x00\x00\x00\x00'
file += b'\x00' * 20
file += b'\x28\x00\x00\x00\x07\x00\x00\x00'

def open_wav(name):
    with open(f'{path}/{name}.wav', 'rb') as infile:
        infile = infile.read()
        size = int.from_bytes(infile[40:44], 'little')
        data = infile[44:]

    return size, data

print('Started (Iniciado)')
offset = 0

size_1, data_1 = open_wav('music01')
size_2, data_2 = open_wav('music02')
size_3, data_3 = open_wav('music03')
size_4, data_4 = open_wav('music04')
size_5, data_5 = open_wav('music05')
size_6, data_6 = open_wav('music06')
size_7, data_7 = open_wav('music07')

file += int(offset).to_bytes(4, 'little')
file += int(size_1).to_bytes(4, 'little')
offset += size_1

file += int(offset).to_bytes(4, 'little')
file += int(size_2).to_bytes(4, 'little')
offset += size_2

file += int(offset).to_bytes(4, 'little')
file += int(size_3).to_bytes(4, 'little')
offset += size_3

file += int(offset).to_bytes(4, 'little')
file += int(size_4).to_bytes(4, 'little')
offset += size_4

file += int(offset).to_bytes(4, 'little')
file += int(size_5).to_bytes(4, 'little')
offset += size_5

file += int(offset).to_bytes(4, 'little')
file += int(size_6).to_bytes(4, 'little')
offset += size_6

file += int(offset).to_bytes(4, 'little')
file += int(size_7).to_bytes(4, 'little')
offset += size_7

file += data_1
file += data_2
file += data_3
file += data_4
file += data_5
file += data_6
file += data_7

output = open(output_name, 'wb')
output.write(file)
output.close()
print('Finished (Terminado)')
