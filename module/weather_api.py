import requests
import urllib.parse
import datetime
import xmltodict # 따로 설치
import pandas as pd # 따로 설치
import json
import timeit

def get_weather():
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    service_key = "n%2BQsBq1EpkbRHO6I5tjZHyBJFOygdGvs2Pyjtdc68xE9Hq2JhqYCa7sGjQyTH5scIQwa3OS40ZL%2FBqoH0amhtQ%3D%3D"

    # 좌표 설정 (서울시 동작구 상도1동)
    x_ssu = "59"
    y_ssu = "125"

    # 날짜/시간 설정
    now = datetime.datetime.now()

    if now.hour == 0 & now.minute <= 30: # 00:00 ~ 00:30
        date_temp = now - datetime.timedelta(days=1)
        base_date = date_temp.strftime("%Y%m%d")
        base_time = "2330"
        #print(base_time)

    elif now.minute <= 30:
        base_date = now.strftime("%Y%m%d")
        time_temp = now - datetime.timedelta(hours=1)
        base_time = time_temp.strftime("%H") + "30"
        #print(base_time)

    else:
        base_date = now.strftime("%Y%m%d")
        base_time = now.strftime("%H30")
        #print(base_time)

    # 초단기예보 데이터 불러오기
    queryParams = "?serviceKey=" + service_key + "&" + urllib.parse.urlencode(
                    {
                        urllib.parse.quote_plus("serviceKey"): urllib.parse.unquote(service_key),
                        urllib.parse.quote_plus("pageNo"): "1",
                        urllib.parse.quote_plus("numOfRows"): "60",
                        urllib.parse.quote_plus("dataType"): "xml",
                        urllib.parse.quote_plus("base_date"): base_date,
                        urllib.parse.quote_plus("base_time"): base_time,
                        urllib.parse.quote_plus("nx"): x_ssu,
                        urllib.parse.quote_plus("ny"): y_ssu
                    }
                )

    # xml 파싱하기
    #print("파싱시작")
    print(url + queryParams)
    res = requests.get(url, queryParams)
    #print("-----------------------------------------------------------------------------------------")
    
    #print(res)
    xml = xmltodict.parse(res.text)
    dict1 = json.loads(json.dumps(xml))
    dict_data = dict1['response']['body']['items']['item']
    #print("파싱 완료")
    # 필요한 데이터: T1H(기온), RN1(1시간 강수량), SKY(하늘상태), PTY(강수형태)
    # 하늘상태(SKY) 코드 : 맑음(1), 구름많음(3), 흐림(4)
    # 강수형태(PTY) 코드 : (초단기) 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7) 

    # fcstTime 생성하기
    fcstTime_tmp = now + datetime.timedelta(hours=1)
    fcstTime = fcstTime_tmp.strftime("%H00")
    #print(fcstTime)

    # 하나의 딕셔너리에 각 시간 별로 리스트 값에 대입
    # 딕셔너리 값은 각각 현재, 2시간뒤, 4시간뒤의 값
    fcst_dict = {"temp": [0, 0, 0], "RN1": [0, 0, 0], "SKY": [0, 0, 0], "PTY": [0, 0, 0]}

    for n in range(42):
        if dict_data[n].get("category") == "T1H" and dict_data[n].get("fcstTime") == fcstTime:  #기온
            fcst_dict["temp"][0] = dict_data[n].get("fcstValue")
            fcst_dict["temp"][1] = dict_data[n+2].get("fcstValue")
            fcst_dict["temp"][2] = dict_data[n+4].get("fcstValue")
            
        elif dict_data[n].get("category") == "RN1" and dict_data[n].get("fcstTime") == fcstTime:    #강수량
            fcst_dict["RN1"][0] = dict_data[n].get("fcstValue")
            fcst_dict["RN1"][1] = dict_data[n+2].get("fcstValue")
            fcst_dict["RN1"][2] = dict_data[n+4].get("fcstValue")

        elif dict_data[n].get("category") == "SKY" and dict_data[n].get("fcstTime") == fcstTime:    #하늘상태
            fcst_dict["SKY"][0] = dict_data[n].get("fcstValue")
            fcst_dict["SKY"][1] = dict_data[n+3].get("fcstValue")
            fcst_dict["SKY"][2] = dict_data[n+5].get("fcstValue")

        elif dict_data[n].get("category") == "PTY" and dict_data[n].get("fcstTime") == fcstTime:    #강수형태
            fcst_dict["PTY"][0] = dict_data[n].get("fcstValue")
            fcst_dict["PTY"][1] = dict_data[n+2].get("fcstValue")
            fcst_dict["PTY"][2] = dict_data[n+4].get("fcstValue")

    return fcst_dict


if __name__ == "__main__":
    start_time = timeit.default_timer()
    a = get_weather()
    print(a)
    terminate_time = timeit.default_timer()
    print("%f초 걸렸습니다." % (terminate_time - start_time))