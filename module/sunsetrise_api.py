import requests
import urllib.parse
import time
import xmltodict # 따로 설치
import json

def get_sunset():
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo"
    service_key = "n%2BQsBq1EpkbRHO6I5tjZHyBJFOygdGvs2Pyjtdc68xE9Hq2JhqYCa7sGjQyTH5scIQwa3OS40ZL%2FBqoH0amhtQ%3D%3D"

    queryParams = "?serviceKey=" + service_key + "&" + urllib.parse.urlencode(
        {
            urllib.parse.quote_plus("serviceKey"): urllib.parse.unquote(service_key),
            urllib.parse.quote_plus("locdate"): time.strftime("%Y%m%d"),
            urllib.parse.quote_plus("location"): "서울"
        }
    )

    #print(url + queryParams) #

    res = requests.get(url, queryParams)
    xml = xmltodict.parse(res.text)
    dict1 = json.loads(json.dumps(xml))
    dict_data = dict1['response']['body']['items']['item']

    sun_list = []
    sun_list.append(int(dict_data["sunrise"]))
    sun_list.append(int(dict_data["sunset"]))
    #print(dict_data)
    #print(sun_list)
    #print(type(sun_list[0]))

    return sun_list

if __name__ == "__main__":
    print(get_sunset())