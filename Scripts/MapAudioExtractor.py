# by: Edu371
# Extrai os Áudios dos Mapas da Campanha, execute primeiro CampaingExtractor
# Extracts Audios from Campaign Maps, first run CampaingExtractor

import os
from os import listdir
from os.path import isfile

path = 'extracted/campaign'
print('Started (Iniciado)')

def save(name, offset, size, header, dict_name):
    data = file[offset:offset+size]
    with open(f'{path}/{dict_name}/{name}', 'wb') as outfile:
        outfile.write(header)
        outfile.write(data)

files = [f for f in listdir(path) if isfile(f'{path}/{f}')]
for a in files:
    if '.map' in a:
        file_name = a 

        file = open(f'{path}/{file_name}', 'rb')
        file = file.read()

        dict_name = file_name[:file_name.find('.')]

        if not os.path.exists(f'{path}/{dict_name}'):
            os.makedirs(f'{path}/{dict_name}')

        offset = int.from_bytes(file[54:58], 'little')
        audio_list = []

        n_audio =  int.from_bytes(file[offset:offset+4], 'little')
        offset += 4

        for _ in range(n_audio):
            a = str(file[offset+44:offset+80], 'utf-8')
            if a.find('\x00') > 0:
                a = a[:a.find('\x00')]
            audio_list.append([a,
                               int.from_bytes(file[offset+180:offset+184], 'little'),
                               int.from_bytes(file[offset+176:offset+180], 'little'),
                               file[offset:offset+44]])
            offset += 184

        for n, x in enumerate(audio_list):
            save(x[0], x[1], x[2], x[3], dict_name)

print('Finished (Terminado)')
