# by: Edu371
# Extrai Mapas da Campanha
# Extracts Campaign Maps

import os

file_name = 'Outlive.dat'

file = open(file_name, 'rb')
file = file.read()

file = file[61241482:113614179]

if not os.path.exists('extracted/campaign'):
    os.makedirs('extracted/campaign')

def save(name, offset):
    size = int.from_bytes(file[offset+8:offset+12], 'little')
    data = file[offset:offset+size]
    data =  data[:53] + b'\x00' + data[54:] # unlocking
    with open(f'extracted/campaign/{name}', 'wb') as outfile:
        outfile.write(data)


header = 14920
offset = 12680
map_list = []

n_maps =  int.from_bytes(file[offset+4:offset+8], 'little')
offset += 8

print('Started (Iniciado)')

for _ in range(n_maps):
    a = str(file[offset:offset+12], 'utf-8')
    if a.find('\x00') > 0:
        a = a[:a.find('\x00')]
    map_list.append([int.from_bytes(file[offset+64:offset+68], 'little'),
                     a])
    offset += 72

for n, x in enumerate(map_list):
    save(x[1], x[0] + header)

print('Finished (Terminado)')
