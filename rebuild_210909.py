from tkinter import *
from tkinter import ttk
import tkinter
import time
from PIL import Image, ImageTk
from module import newsfeed, weather_api, sunsetrise_api

font_L = ("맑은 고딕", 80)


class Clock(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, background="black")

        self.time_label = ttk.Label(self, font=Board.largeFont, background="black", foreground="white")
        self.time_label.pack()
        self.date_label = ttk.Label(self, font=Board.normalFont, background="black", foreground="white")
        self.date_label.pack()
        
        self.digit_clock()

    def digit_clock(self):
        yoil = ["월", "화", "수", "목", "금", "토", "일"]
        today = yoil[time.localtime().tm_wday]
        self.time_label.configure(text=time.strftime("%H:%M:%S"))
        self.date_label.configure(text=time.strftime("%m월 %d일 ") + "(" + today + ")")
        self.time_label.after(200, self.digit_clock)

class Weather(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, background="black")

        self.tempnow_label = ttk.Label(self, font=Board.largeFont, background="black", foreground="white")
        self.tempnow_label.pack(side="right")
        self.icon_label = ttk.Label(self, background="black")
        self.icon_label.pack(side="left")

        self.updateWeather()

    def updateWeather(self):
        img = Image.open("assets/sunny.png")
        photo = ImageTk.PhotoImage(img)
        self.tempnow_label.configure(text=weather_api.get_weather()["temp"][0] + "°C")
        self.tempnow_label.after(600000, self.updateWeather)
        self.icon_label.configure(image=photo)
        self.icon_label.image = photo

class News(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, background="black")

        self.news_label = ttk.Label(self, font=Board.middleFont, background="black", foreground="white")
        self.news_label.pack(anchor="center")

        self.updateNews()

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


class Board:
    def __init__(self) -> None:
        self.tk = Tk()
        self.tk.title("Smart Mirror")
        self.tk.geometry("1920x1080")
        self.tk.resizable(True, True)

        Board.cnt = 0

        # 글꼴
        Board.largeFont = ("맑은 고딕", 80)
        Board.middleFont = ("맑은 고딕", 45)
        Board.normalFont = ("맑은 고딕", 30)

        # 시간/날짜
        clock_frame = Frame(self.tk, bg="black")
        clock_frame.pack(side="top", fill="both")
        self.clock = Clock(clock_frame)
        self.clock.pack()

        # 뉴스
        news_frame = Frame(self.tk, height=300, bg='black')
        news_frame.pack(side="bottom", fill="both")
        self.news = News(news_frame)
        self.news.pack()

        # 날씨
        weather_frame = Frame(self.tk, bg='red')
        weather_frame.pack(side="left", fill="y")
        self.weather = Weather(weather_frame)
        self.weather.pack()

        # 일정
        schedule_frame = Frame(self.tk, bg='blue')
        schedule_frame.pack(side="right", fill="y")

        self.tk.attributes("-fullscreen", True)

        self.tk.bind("<F11>", lambda event: self.tk.attributes("-fullscreen", not self.tk.attributes("-fullscreen")))
        self.tk.bind("<Escape>", lambda event: self.tk.attributes("-fullscreen", False))
        





if __name__ == "__main__":
    window = Board()
    window.tk.mainloop()