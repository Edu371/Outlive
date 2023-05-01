# by: Edu371
# exibe secções e suas posições
# shows sections and their offsets

file_name = 'Outlive.dat'

content = open(file_name, 'rb')
content = content.read()
content = content[:4108]

l = []

chunk = 36
chunks = int.from_bytes(content[:4], 'little')

for n in range(chunks):
    a = content[chunk*n+4:chunk*n+chunk+4]
    pos = int.from_bytes(a[32:], 'little')
    string = str(a[:32], 'utf-8')
    l.append([string, pos])

l = sorted(l, key=lambda x: x[1])

for x in l:
    print(x[0], x[1])

