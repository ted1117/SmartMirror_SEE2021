from tkinter import *
from tkinter import ttk
import tkinter.font
import time

# 속성
root = tkinter.Tk()
root.title("Smart Mirror")
root.geometry("1920x1080")
root.configure(background="black")
root.resizable(False, False)
#largeFont = ("Boulder", 68, 'bold')
#mediumFont = ("MalgunGothic", 50)
#normalFont = ("MalgunGothic", 30)

WIDTH = 1920
HEIGHT = 1080


class Board(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.largeFont = tkinter.font.Font(family="Piboto", size=70)
        self.mediumFont = tkinter.font.Font(family="Piboto", size=40)
        self.normalFont = tkinter.font.Font(family="Piboto Light", size=20)

    def Clock(self):
        self.grid()

        time_frame = Frame(self, width=400, height=500, bg="white")
        time_frame.grid(row=0, column=2, sticky=NE)
        self.time_label = ttk.Label(time_frame, font=self.largeFont, background="black", foreground="white")
        self.time_label.grid(row=0, column=1, sticky=NE)
        self.date_label = ttk.Label(time_frame, font=self.normalFont, background="black", foreground="white")
        self.date_label.grid(row=1, column=1, sticky=NE)

    # 기능
    def digit_clock(self):
        self.time_label.configure(text=time.strftime("%H:%M:%S"))
        self.date_label.configure(text=time.strftime("%m월 %d일"))
        self.time_label.after(200, self.digit_clock)

mirror = Board(root)
mirror.Clock()
mirror.digit_clock()
root.mainloop()
