# by: Edu371
# Vídeo Player Simples
# Simple Video Player

from tkinter import *
import pyaudio
from _thread import start_new_thread
import time
from PIL import ImageTk, Image

class Clock:
    
    def __init__(self, fps):
        self.start = time.perf_counter()
        self.frame_length = 1/fps
    @property
    def tick(self):
        return int((time.perf_counter() - self.start)/self.frame_length)

    def sleep(self):
        r = self.tick + 1
        while self.tick < r:
            time.sleep(1/1000)

class Player:
    def __init__(self, frames, audio, fps, size, legenda={}, upscale=False,
                 alpha=False):

        print('Iniciando Player')
        self.audio = audio
        self.frames = frames
        self.fps = fps
        self.legenda = legenda
        self.clock = None

        
        self.main = Tk()
        if upscale:
            size[0] *= upscale
            size[1] *= upscale
            self.upscaler(upscale)
        self.main.geometry(f'{size[0]}x{size[1] + 125}+0+0')
        self.main.title('Paf Player')
        self.main.resizable(False, False)
        self.main.wm_minsize(200, 200)

        if alpha:
            self.paster()

        for n in range(len(frames)):
            frames[n] = ImageTk.PhotoImage(frames[n])
        
        p = pyaudio.PyAudio()
        self.audio_player = p.open(format=pyaudio.paInt16, channels=1, rate=22050,
                            output=True)

        self.canvas = Canvas(self.main, width=size[0], height=size[1], bg='black',
                        highlightthickness=0)
        self.canvas.pack()

        self.main.img = frames[0]
        self.view = self.canvas.create_image(size[0]/2, size[1]/2,
                                             image=self.main.img)
        
        self.leg_label = Label(self.main, text='', wraplengt=size[0])
        self.leg_label.pack()
        self.frame_label = Label(self.main, text='0')
        self.frame_label.pack()
        self.play_button = Button(self.main, text='Play', command=self.play)
        self.play_button.pack()
        self.restart_button = Button(self.main, text='Restart', command=self.restart)
        self.restart_button.pack()
        self.playing = False
        self.main.mainloop()

    def play(self):
        if self.playing:
            self.playing = False
            self.play_button['text'] = 'Play'

        else:
            self.playing = True
            self.play_button['text'] = 'Pause'
            start_new_thread(self.play_audio, ())
            self.play_image()
            
    def change_legenda(self, x):
        if x in self.legenda:
            self.leg_label['text'] = self.legenda[x][1]

    def play_audio(self):
        x = 0
        if len(self.audio):
                while self.playing and x < len(self.audio):
                    self.audio_player.write(self.audio[x: x+44100])
                    x += 44100
    
    def play_image(self):
        total = time.perf_counter()
        self.clock = Clock(self.fps)
        for n, x in enumerate(self.frames):
            if not self.playing:
                break
            timer = time.perf_counter_ns()
            self.main.img = x
            self.canvas.itemconfig(self.view, image=self.main.img)
            self.frame_label['text'] = str(n)
            if n in self.legenda:
                self.change_legenda(n)
            self.main.update()
            self.clock.sleep()
            #time.sleep(1 /self.fps)
            print(time.perf_counter_ns() - timer)
        if self.playing:
            self.play()
        print(time.perf_counter() - total)

    def upscaler(self, ratio):
        for n, x in enumerate(self.frames):
            self.frames[n] = x.resize((x.size[0]*ratio, x.size[1]*ratio))

    def paster(self):
        for n in range(len(self.frames)-1):
            x = self.frames[n+1]
            self.frames[n+1] = Image.alpha_composite(self.frames[n], x)

    def restart(self):
        self.play()
        self.play()
