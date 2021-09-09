from tkinter import *
from tkinter import ttk
import tkinter
import time
from PIL import Image, ImageTk
from module import newsfeed, weather_api, sunsetrise_api

# 속성
root = tkinter.Tk()
root.title("Smart Mirror")
root.geometry("1920x1080")
#root.configure(background="black")
root.resizable(True, True)

class Board(Frame):
    cnt = 0
    # 전체 GUI 구현
    def __init__(self, master):
        Frame.__init__(self, master)

        self.pack(expand=True, fill=BOTH)
        
        # 글꼴
        self.largeFont = ("맑은 고딕", 80)
        self.middleFont = ("맑은 고딕", 45)
        self.normalFont = ("맑은 고딕", 30)

        # 시간/날짜
        clock_frame = Frame(self, bg="black")
        clock_frame.pack(side="top", fill="both")
        self.time_label = ttk.Label(clock_frame, font=self.largeFont, background="black", foreground="white")
        self.time_label.pack()
        self.date_label = ttk.Label(clock_frame, font=self.normalFont, background="black", foreground="white")
        self.date_label.pack()

        # 뉴스
        news_frame = Frame(self, height=300, bg='black')
        news_frame.pack(side="bottom", fill="both")
        self.news_label = ttk.Label(news_frame, font=self.middleFont, background="black", foreground="white")
        self.news_label.pack(anchor="center")

        # 날씨
        weather_frame = Frame(self, bg='red')
        weather_frame.pack(side="left", fill="y")
        self.tempnow_label = ttk.Label(weather_frame, font=self.largeFont, background="black", foreground="white")
        self.tempnow_label.pack(side="right")

        # 일정
        schedule_frame = Frame(self, bg='blue')
        schedule_frame.pack(side="right", fill="y")
        self.schedule_label = ttk.Label(schedule_frame, font=self.largeFont, background="black", foreground="white", text="schedule")
        self.schedule_label.pack(anchor="center")

    # 시계 기능
    def digit_clock(self):
        yoil = ["월", "화", "수", "목", "금", "토", "일"]
        today = yoil[time.localtime().tm_wday]
        self.time_label.configure(text=time.strftime("%H:%M:%S"))
        self.date_label.configure(text=time.strftime("%m월 %d일 ") + "(" + today + ")")
        self.time_label.after(200, self.digit_clock)

    # 날씨 기능
    def updateWeather(self):
        self.tempnow_label.configure(text=weather_api.get_weather()["temp"][0] + "°C")
        self.tempnow_label.after(600000, self.updateWeather)

    # 뉴스 기능
    def updateNews(self):
        num_of_news = len(newsfeed.get_newsfeed()) - 1
        if Board.cnt < num_of_news:
            self.news_label.configure(text=newsfeed.get_newsfeed()[Board.cnt])
            Board.cnt += 1
            self.news_label.after(3000, self.updateNews)
        else:
            self.news_label.configure(text=newsfeed.get_newsfeed()[num_of_news])
            Board.cnt = 0
            self.news_label.after(3000, self.updateNews)
        
        

# 실행
mirror = Board(root)
mirror.digit_clock()
mirror.updateWeather()
mirror.updateNews()
root.attributes("-fullscreen", True)

root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
root.mainloop()