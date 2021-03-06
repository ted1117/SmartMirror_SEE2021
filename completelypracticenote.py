from tkinter import * 
from tkinter import ttk
import time, datetime
from PIL import Image, ImageTk
from module import newsfeed, weather_api, sunsetrise_api, gcalendar, PMstatus_api, covid19cnt_api, busarri_api

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

        fcstTime2_tmp = datetime.datetime.now() + datetime.timedelta(hours=3)
        fcstTime4_tmp = datetime.datetime.now() + datetime.timedelta(hours=5)
        fcstTime2 = fcstTime2_tmp.strftime("%H시")
        fcstTime4 = fcstTime4_tmp.strftime("%H시")

        global weather_dict
        weather_dict = weather_api.get_weather()

        # 현재 날씨
        self.icon_label = ttk.Label(self, background="black")
        self.icon_label.grid(column=0, row=0, columnspan=2)
        self.temp_label = ttk.Label(self, font=Board.largeFont, background="black", foreground="white")
        self.temp_label.grid(column=2, row=0, columnspan=4)
        self.wth_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.wth_label.grid(column=5, row=1)
        self.PM25_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white", text="미세")
        self.PM25_label.grid(column=2, row=2)
        self.PM25grd_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.PM25grd_label.grid(column=3, row=2)
        self.PM10_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white", text="• 초미세")
        self.PM10_label.grid(column=4, row=2)
        self.PM10grd_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.PM10grd_label.grid(column=5, row=2)
        s1 = ttk.Separator(self, orient='horizontal')
        s1.grid(column=0, row=3, sticky="ew", columnspan=6)

        # 2시간 뒤 날씨
        self.time2_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white", text=fcstTime2)
        self.time2_label.grid(column=0, row=4)
        s11 = ttk.Separator(self, orient="vertical")
        s11.grid(column=1, row=4, sticky="ns", rowspan=4)
        self.wth2_icon = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.wth2_icon.grid(column=2, row=4)
        self.wth2_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.wth2_label.grid(column=3, row=4)
        self.temp2_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.temp2_label.grid(column=5, row=4)
        s2 = ttk.Separator(self, orient='horizontal')
        s2.grid(column=0, row=5, sticky="ew", columnspan=6)

        # 4시간 뒤 날씨
        self.time4_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white", text=fcstTime4)
        self.time4_label.grid(column=0, row=6)
        self.wth4_icon = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.wth4_icon.grid(column=2, row=6)
        self.wth4_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.wth4_label.grid(column=3, row=6)
        self.temp4_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.temp4_label.grid(column=5, row=6)
        s3 = ttk.Separator(self, orient='horizontal')
        s3.grid(column=0, row=7, sticky="ew", columnspan=6)
        
        self.updatePMgrade()
        self.updateWeather()
        self.WeatherIn2()
        self.WeatherIn4()

    def updatePMgrade(self):
        pm25 = PMstatus_api.getPMstatus()["pm25Grade"]
        pm10 = PMstatus_api.getPMstatus()["pm10Grade"]

        if pm25 == "1":
            self.PM25grd_label.configure(text="좋음", foreground="skyblue")
        elif pm25 == "2":
            self.PM25grd_label.configure(text="보통", foreground="green")
        elif pm25 == "3":
            self.PM25grd_label.configure(text="나쁨", foreground="orange")
        elif pm25 == "4":
            self.PM25grd_label.configure(text="매우나쁨", foreground="red")

        if pm10 == "1":
            self.PM10grd_label.configure(text="좋음", foreground="skyblue")
        elif pm10 == "2":
            self.PM10grd_label.configure(text="보통", foreground="green")
        elif pm10 == "3":
            self.PM10grd_label.configure(text="나쁨", foreground="orange")
        elif pm10 == "4":
            self.PM10grd_label.configure(text="매우나쁨", foreground="red")
        
        self.PM10grd_label.after(1800000, self.updatePMgrade)

    def updateWeather(self):
        self.temp_label.configure(text=" " + weather_dict["temp"][0] + "°C")
        self.temp_label.after(600000, self.updateWeather)
        
        # 현재 날씨 아이콘
        if weather_dict["SKY"][0] == "1":
            if (sunsetrise_api.get_sunset()[0] < int(time.strftime("%H%M")) < sunsetrise_api.get_sunset()[1]):
                photo = ImageTk.PhotoImage(Image.open("assets/clear_day.png"))
                self.icon_label.configure(image=photo)
            else:
                photo = ImageTk.PhotoImage(Image.open("assets/clear_night.png"))
                self.icon_label.configure(image=photo)
            self.wth_label.configure(text="맑음")

        elif weather_dict["SKY"][0] == "3":
            if (sunsetrise_api.get_sunset()[0] < int(time.strftime("%H%M")) < sunsetrise_api.get_sunset()[1]):
                photo = ImageTk.PhotoImage(Image.open("assets/cloudy_day.png"))
                self.icon_label.configure(image=photo)
            else:
                photo = ImageTk.PhotoImage(Image.open("assets/cloudy_night.png"))
                self.icon_label.configure(image=photo)
            self.wth_label.configure(text="구름많음")
        
        elif weather_dict["SKY"][0] == "4":
            photo = ImageTk.PhotoImage(Image.open("assets/too_cloudy.png"))
            self.icon_label.configure(image=photo)
            self.wth_label.configure(text="흐림")

        elif weather_dict["PTY"][0] == "1":
            photo = ImageTk.PhotoImage(Image.open("assets/rainy2.png"))
            self.icon_label.configure(image=photo)
            self.wth_label.configure(text="비")

        elif weather_dict["PTY"][0] == "2":
            photo = ImageTk.PhotoImage(Image.open("assets/snowy.png"))
            self.icon_label.configure(image=photo)
            self.wth_label.configure(text="비/눈")

        elif weather_dict["PTY"][0] == "3":
            photo = ImageTk.PhotoImage(Image.open("assets/snowy2.png"))
            self.icon_label.configure(image=photo)
            self.wth_label.configure(text="눈")

        elif weather_dict["PTY"][0] == "5":
            photo = ImageTk.PhotoImage(Image.open("assets/rainy.png"))
            self.icon_label.configure(image=photo)          
            self.wth_label.configure(text="비")

        self.icon_label.image = photo

    def WeatherIn2(self):
        self.temp2_label.configure(text=weather_dict["temp"][1] + "°C")
        self.temp2_label.after(600000, self.WeatherIn2)
        width = 50
        height = 50

        # 2시간 뒤 날씨 아이콘
        if weather_dict["SKY"][1] == "1":
            if (sunsetrise_api.get_sunset()[0] < int(time.strftime("%H%M")) < sunsetrise_api.get_sunset()[1]):
                img = Image.open('assets/clear_day.png')
                icon = ImageTk.PhotoImage(img.resize((width, height)))
            else:
                img = Image.open("assets/clear_night.png")
                icon = ImageTk.PhotoImage(img.resize((width, height)))
            self.wth2_label.configure(text="맑음")

        elif weather_dict["SKY"][1] == "3":
            if (sunsetrise_api.get_sunset()[0] < int(time.strftime("%H%M")) < sunsetrise_api.get_sunset()[1]):
                img = Image.open('assets/cloudy_day.png')
                icon = ImageTk.PhotoImage(img.resize((width, height)))
            else:
                img = Image.open("assets/cloudy_night.png")
                icon = ImageTk.PhotoImage(img.resize((width, height)))
            self.wth2_label.configure(text="구름많음")
        
        elif weather_dict["SKY"][1] == "4":
            img = Image.open("assets/too_cloudy.png")
            icon = ImageTk.PhotoImage(img.resize((width, height)))
            self.wth2_label.configure(text="흐림")

        elif weather_dict["PTY"][1] == "1":
            img = Image.open("assets/rainy2.png")
            icon = ImageTk.PhotoImage(img.resize((width, height)))
            self.wth2_label.configure(text="비")

        elif weather_dict["PTY"][1] == "2":
            img = Image.open("assets/snowy.png")
            icon = ImageTk.PhotoImage(img.resize((width, height)))
            self.wth2_label.configure(text="비/눈")

        elif weather_dict["PTY"][1] == "3":
            img = Image.open("assets/snowy2.png")
            icon = ImageTk.PhotoImage(img.resize((width, height)))
            self.wth2_label.configure(text="눈")

        elif weather_dict["PTY"][1] == "5":
            img = Image.open("assets/rainy.png")
            icon = ImageTk.PhotoImage(img.resize((width, height)))
            self.wth2_label.configure(text="비")

        self.wth2_icon.configure(image=icon)
        self.wth2_icon.image = icon

    def WeatherIn4(self):
        self.temp4_label.configure(text=weather_dict["temp"][2] + "°C")
        self.temp4_label.after(600000, self.WeatherIn4)
        width = 50
        height = 50

        # 4시간 뒤 날씨 아이콘
        if weather_dict["SKY"][2] == "1":
            if (sunsetrise_api.get_sunset()[0] < int(time.strftime("%H%M")) < sunsetrise_api.get_sunset()[1]):
                img2 = Image.open('assets/clear_day.png')
                icon2 = ImageTk.PhotoImage(img2.resize((width, height))) 
            else:
                img2 = Image.open("assets/clear_night.png")
                icon2 = ImageTk.PhotoImage(img2.resize((width, height)))
            self.wth4_label.configure(text="맑음")

        elif weather_dict["SKY"][2] == "3":
            if (sunsetrise_api.get_sunset()[0] < int(time.strftime("%H%M")) < sunsetrise_api.get_sunset()[1]):
                img2 = Image.open('assets/cloudy_day.png')         
                icon2 = ImageTk.PhotoImage(img2.resize((width, height)))
            else:
                img2 = Image.open("assets/cloudy_night.png")
                icon2 = ImageTk.PhotoImage(img2.resize((width, height)))           
            self.wth4_label.configure(text="구름많음")
        
        elif weather_dict["SKY"][2] == "4":
            img2 = Image.open("assets/too_cloudy.png")
            icon2 = ImageTk.PhotoImage(img2.resize((width, height)))
            self.wth4_label.configure(text="흐림")

        elif weather_dict["PTY"][2] == "1":
            img2 = Image.open("assets/rainy2.png")
            icon2 = ImageTk.PhotoImage(img2.resize((width, height)))
            self.wth4_label.configure(text="비")

        elif weather_dict["PTY"][2] == "2":
            img2 = Image.open("assets/snowy.png")
            icon2 = ImageTk.PhotoImage(img2.resize((width, height)))
            self.wth4_label.configure(text="비/눈")

        elif weather_dict["PTY"][2] == "3":
            img2 = Image.open("assets/snowy2.png")
            icon2 = ImageTk.PhotoImage(img2.resize((width, height)))
            self.wth4_label.configure(text="눈")

        elif weather_dict["PTY"][2] == "5":
            img2 = Image.open("assets/rainy.png")
            icon2 = ImageTk.PhotoImage(img2.resize((width, height)))
            self.wth4_label.configure(text="비")
            
        self.wth4_icon.configure(image=icon2)
        self.wth4_label.image = icon2

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

class Calendar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, background="black")

        self.schedule_label = ttk.Label(self, font=Board.middleFont, background="black", foreground="white", text="오늘 일정")        
        self.schedule_label.grid(column=0, row=0)
        s4 = ttk.Separator(self, orient='horizontal')
        s4.grid(column=0, row=1, sticky="ew")

        self.todo1_tlabel = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.todo1_tlabel.grid(column=0, row=2, sticky="w")
        self.todo1_slabel = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.todo1_slabel.grid(column=0, row=2, sticky="e")
        s5 = ttk.Separator(self, orient='horizontal')
        #s5.grid(column=0, row=3, sticky="ew")

        self.todo2_tlabel = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.todo2_tlabel.grid(column=0, row=4, sticky="w")
        self.todo2_slabel = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.todo2_slabel.grid(column=0, row=4, sticky="e")
        s6 = ttk.Separator(self, orient="horizon")
        #s6.grid(column=0, row=5, sticky="ew")

        self.todo3_tlabel = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.todo3_tlabel.grid(column=0, row=6, sticky="w")
        self.todo3_slabel = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.todo3_slabel.grid(column=0, row=6, sticky="e")

        self.arvinfo_label =  ttk.Label(self, font=Board.middleFont, background="black", foreground="white", text="숭실대정문")
        self.arvinfo_label.grid(column=0, row=8)
        s5 = ttk.Separator(self, orient='horizontal')
        s5.grid(column=0, row=9, sticky="ew")
        self.bus1_label = ttk.Label(self, font=Board.smallFont, background="blue", foreground="white", text="742")    
        self.bus1_label.grid(column=0, row=10, sticky="w")
        self.bus2_label = ttk.Label(self, font=Board.smallFont, background="blue", foreground="white", text="742")    
        self.bus2_label.grid(column=0, row=11, sticky="w")
        self.ETA1_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")    
        self.ETA1_label.grid(column=0, row=10, sticky="e")
        self.ETA2_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")  
        self.ETA2_label.grid(column=0, row=11, sticky="e")
        self.blank_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")

        self.updateTodo()
        self.getETAinfo()
        self.updateETA()

    def updateTodo(self):
        self.schedule_label.after(10000000, self.updateTodo)

        tlabel_list = [self.todo1_tlabel, self.todo2_tlabel, self.todo3_tlabel]
        slabel_list = [self.todo1_slabel, self.todo2_slabel, self.todo3_slabel]

        for n in range(len(gcalendar.getTodo())):
            tlabel = tlabel_list[n]
            slabel = slabel_list[n]
            tlabel.configure(text=gcalendar.getTodo()[n]["start"])
            slabel.configure(text=gcalendar.getTodo()[n]["summary"])
    
    def getETAinfo(self):
        '''
        Calendar.ETA = busarri_api.update_busarr()

        if Calendar.ETA == 0:
            self.ETA1_label.configure(text="출발 대기")
            self.blank_label.after(180000, self.getETAinfo)'''
        
        Calendar.ETA1 = busarri_api.update_busarr()[0]
        Calendar.ETA2 = busarri_api.update_busarr()[1]
        Calendar.msg1 = busarri_api.update_busarr()[2]

        if Calendar.ETA1 == 0:
            self.ETA1_label.configure(text=busarri_api.update_busarr()[2])
            self.blank_label.after(180000, self.getETAinfo)
        
        if Calendar.ETA2 <= 0:
            self.ETA2_label.configure(text=busarri_api.update_busarr()[3])

        #self.blank_label.after(300000, self.getETAinfo)

    def updateETA(self):
        ETA1_min = str(Calendar.ETA1//60)
        ETA1_sec = str(Calendar.ETA1%60)
        ETA2_min = str(Calendar.ETA2//60)
        ETA2_sec = str(Calendar.ETA2%60)

        if Calendar.msg1 == "곧 도착":
            self.ETA1_label.configure(text=Calendar.msg1)
            if ETA2_min == "0":
                self.ETA2_label.configure(text=ETA2_sec + "초")
                Calendar.ETA2 -= 1
            else:
                self.ETA2_label.configure(text=ETA2_min + "분" + " " + ETA1_sec + "초")
                Calendar.ETA2 -= 1
            self.ETA2_label.after(1000, self.updateETA)
        
        elif Calendar.msg1 != "곧 도착":
            if ETA1_min == "0":
                self.ETA1_label.configure(text=ETA1_sec + "초")
                Calendar.ETA1 -= 1

            else:
                self.ETA1_label.configure(text=ETA1_min + "분" + " " + ETA1_sec + "초")
                Calendar.ETA1 -= 1
        
            if ETA2_min == "0":
                self.ETA2_label.configure(text=ETA2_sec + "초")
                Calendar.ETA2 -= 1

            else:
                self.ETA2_label.configure(text=ETA2_min + "분" + " " + ETA1_sec + "초")
                Calendar.ETA2 -= 1

        if (Calendar.ETA1 <= 0) & (Calendar.msg1 != "운행 종료"):
            self.getETAinfo()
            self.ETA1_label.after(1000, self.updateETA) 
        

        self.ETA1_label.after(1000, self.updateETA) 

class Covid19(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, background="blue")

        self.cnt_label = ttk.Label(self, font=Board.smallFont, background="black", foreground="white")
        self.cnt_label.pack()

        self.updateDCDcnt()

    def updateDCDcnt(self):
        self.cnt_label.configure(text="코로나19 신규 확진자: " + str(covid19cnt_api.getDCDcnt()))    

class Board:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Smart Mirror")
        self.tk.geometry("1920x1080")
        self.tk.configure(background="black")
        self.tk.resizable(True, True)

        Board.cnt = 0

        # 글꼴
        Board.largeFont = ("맑은 고딕", 80)
        Board.middleFont = ("맑은 고딕", 45)
        Board.normalFont = ("맑은 고딕", 30)
        Board.smallFont = ("맑은 고딕", 20)

        # 시간/날짜
        clock_frame = Frame(self.tk, bg="black")
        clock_frame.pack(side="top", fill="both")
        Clock(clock_frame).pack()   

        # 뉴스
        news_frame = Frame(self.tk, height=300, bg='black')
        news_frame.pack(side="bottom", fill="both")
        News(news_frame).pack()

        # 코로나19
        covid_frame = Frame(self.tk, bg="blue")
        covid_frame.pack(side="bottom", fill="both")
        Covid19(covid_frame).pack()
        
        # 날씨
        weather_frame = Frame(self.tk, bg='black')
        weather_frame.pack(side="left", fill="y")
        Weather(weather_frame).pack()

        # 일정
        schedule_frame = Frame(self.tk, bg='black')
        schedule_frame.pack(side="right", fill="y")
        Calendar(schedule_frame).pack()

        self.tk.attributes("-fullscreen", True)

        self.tk.bind("<F11>", lambda event: self.tk.attributes("-fullscreen", not self.tk.attributes("-fullscreen")))
        self.tk.bind("<Escape>", lambda event: self.tk.attributes("-fullscreen", False))

if __name__ == "__main__":
    window = Board()
    window.tk.mainloop()