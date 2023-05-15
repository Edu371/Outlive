# by: Edu371
# Exibe Creditos em Janela Tkinter
# Shows Credits in Tkinter  Window

from tkinter import *


file_name = 'Outlive.dat'
print('Started (Iniciado)')

file = open(file_name, 'rb')
file = file.read()

file = file[113614179:113622304]

offset = 21
text_count = int.from_bytes(file[4:8] ,'little')
header = 21 + text_count * 15
colors = [hex(int.from_bytes(file[12:15] ,'big'))[2:].zfill(6),
          hex(int.from_bytes(file[15:18] ,'big'))[2:].zfill(6),
          hex(int.from_bytes(file[18:21] ,'big'))[2:].zfill(6)]

class ScrollableFrame:
    def __init__(self):
        self.main = Tk()
        self.main.title('Credits')

        mainFrame = Frame(self.main)
        mainFrame.pack()

        self.canvas = Canvas(mainFrame, bg='Black', width=640, height=480)
        self.canvas.pack(side='left')

        scroll_y = Scrollbar(mainFrame, orient="vertical", command=self.canvas.yview)
        scroll_y.pack(fill='y', side='right')

        self.insideFrame = Frame(self.canvas, bg='black', width=640, height=480)
        self.insideFrame.pack_propagate(False)

        self.canvas.create_window((0, 0), anchor='nw', window=self.insideFrame)

        self.main.update()

        self.canvas.configure(scrollregion=self.canvas.bbox('all'),
                              yscrollcommand=scroll_y.set)

    def create_label(self, text, size, color):
            label = Label(self.insideFrame, text=text, fg=f'#{color}', bg='black',
                  font=('Arial', 10+size*2))
            label.pack(side='top')
            self.canvas.update_idletasks()
            self.insideFrame['height'] = self.insideFrame.winfo_height() + label.winfo_height()
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))
            self.canvas.update_idletasks()


def read_text(text_offset):
    text = b''
    char = file[text_offset:text_offset+1]
    while char != b'\x00':
        text += char
        text_offset += 1
        char = file[text_offset:text_offset+1]

    return str(text, 'iso-8859-1')


window = ScrollableFrame()

for x in range(text_count):
    text_offset = int.from_bytes(file[offset:offset+4] ,'little') + header
    text_size = file[offset+4]
    text_color = file[offset+5]
    text = read_text(text_offset)
    window.create_label(text, text_size, colors[text_color])
    offset += 15

print('Finished (Terminado)')

window.main.mainloop()
