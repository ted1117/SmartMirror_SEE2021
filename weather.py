import requests
import urllib.parse
import datetime
#from datetime import timedelta, datetime
import xmltodict
import pandas as pd
import json

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
    print(base_time)

elif now.minute <= 30:
        base_date = now.strftime("%Y%m%d")
        time_temp = now - datetime.timedelta(hours=1)
        base_time = time_temp.strftime("%H") + "30"
        print(base_time)

else:
    base_date = now.strftime("%Y%m%d")
    base_time = now.strftime("%H%M")
    print(base_time)

# 초단기실황 데이터 불러오기
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

res = requests.get(url, queryParams).content
print(url + queryParams)
print()
print()
print()
print()
#print(res)
xml = xmltodict.parse(res)
dict1 = json.loads(json.dumps(xml))
dict_data = dict1['response']['body']['items']['item']
print(dict_data[0])

for n in range(50):
    pass

#print(dict_data)

# 엑셀로 저장하기
#df = pd.DataFrame(dict_data)
#df.to_excel(excel_writer="get_weather.xlsx")