# -*- conding: utf-8 -*-
from tkinter import *
from tkinter import ttk
import tkinter
import time
from module import weather_api

# 속성
root = tkinter.Tk()
root.title("Smart Mirror")
root.geometry("1920x1080")
root.configure(background="black")
root.resizable(False, False)

class Board(Frame):
    # 전체 GUI 구현
    def __init__(self, master):
        Frame.__init__(self, master)

        self.grid()
        
        # 글꼴
        self.largeFont = ("MalgunGothic", 68)
        self.normalFont = ("MalgunGothic", 30)

        # 시간/날짜
        clock_frame = Frame(self, width=400, height=500, bg="black")
        clock_frame.grid(row=0, column=2, sticky=NE)
        self.time_label = ttk.Label(clock_frame, font=self.largeFont, background="black", foreground="white")
        self.time_label.grid(row=0, column=1, sticky=NE)
        self.date_label = ttk.Label(clock_frame, font=self.normalFont, background="black", foreground="white")
        self.date_label.grid(row=1, column=1, sticky=N)

        # 날씨
        #weather_frame = Frame(self, width=400, height=500, bg="white")
        #weather_frame.grid(row=2, column=2)
        #self.weather_label = ttk.Label(weather_frame, font=self.largeFont, background="black", foreground="white")

    # 시계 기능
    def digit_clock(self):
        self.time_label.configure(text=time.strftime("%H:%M:%S"))
        self.date_label.configure(text=time.strftime("%m월 %d일"))
        self.time_label.after(200, self.digit_clock)

    # 날씨 기능
    def updateWeather(self):
        self.weather_label.configure(text=time.strftime("%H:%M:%S"))
        self.weather_label.after(200, self.updateWeather)

# 실행
mirror = Board(root)
mirror.digit_clock()
#mirror.updateWeather()
root.mainloop()