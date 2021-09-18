"""
일출/일몰시간을 통해 오늘의 낮시간을 알기 위한 모듈.
"""

import requests
import urllib.parse
import time
import xmltodict # 따로 설치
import json

def get_sunset():
    """
    한국천문연구원에서 제공하는 데이터 中 오늘의 일출/일몰 시간을 int로 변환하고 리스트에 추가
    오늘의 일출/일몰 시간이 포함된 sun_list가 리턴됨.
    """
    # secret_key.json에 저장된 일반 인증키(Encoding)를 불러오기
    with open("module/secret_key.json") as json_file:
        json_data = json.load(json_file)

    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo"
    service_key = json_data

    queryParams = "?" + urllib.parse.urlencode({
            urllib.parse.quote_plus("serviceKey"): urllib.parse.unquote(service_key),
            urllib.parse.quote_plus("locdate"): time.strftime("%Y%m%d"),
            urllib.parse.quote_plus("location"): "서울"
        })

    res = requests.get(url + queryParams)
    xml = xmltodict.parse(res.text)
    dict1 = json.loads(json.dumps(xml))
    dict_data = dict1['response']['body']['items']['item']

    sun_list = []
    sun_list.append(int(dict_data["sunrise"]))
    sun_list.append(int(dict_data["sunset"]))

    return sun_list


if __name__ == "__main__":
   print(get_sunset())
   print(get_sunset().__doc__)