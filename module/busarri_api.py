import requests
import urllib.parse
import datetime
import xmltodict # 따로 설치
import json
import time

def update_busarr():
    """
    초단기예보조회에서 불러온 날씨 데이터를 딕셔너리에 추가

    기온, 강수량, 하늘상태, 강수형태의 리스트를 추가한 딕셔너리 fcst_dict를 리턴함.
    """
    # secret.json에 저장된 일반 인증키(Encoding)를 불러오기
    with open("secret.json") as json_file:
        json_data = json.load(json_file)

    url = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll'
    service_key = json_data

    stId = "20170"
    busRouteId = "100100116"
    stord = "80"

    # 숭실대정문(20170)의 742 도착정보 불러오기
    '''queryParams = "?" + urllib.parse.urlencode({
                        urllib.parse.quote_plus("serviceKey"): urllib.parse.unquote(service_key),
                        urllib.parse.quote_plus("stId"): stId,
                        urllib.parse.quote_plus("busRouteId"): busRouteId,
                        urllib.parse.quote_plus("ord"): stord
                    })'''
    queryParams = "?" + urllib.parse.urlencode({
                        urllib.parse.quote_plus("serviceKey"): urllib.parse.unquote(service_key),
                        urllib.parse.quote_plus("busRouteId"): busRouteId
                    })

    print(url + queryParams)
    res = requests.get(url + queryParams)
    xml = xmltodict.parse(res.text)
    dict1 = json.loads(json.dumps(xml))
    dict_data = dict1['ServiceResult']['msgBody']['itemList']
    
    #print(dict_data)

    data = dict_data[0]["arsId"]
    print(data)
    for data in dict_data:
        if data["arsId"] == "20170":
            ETA1 = int(data["traTime1"])
            ETA2 = int(data["traTime2"])
            msg1 = data["arrmsg1"]
            msg2 = data["arrmsg2"]

    ETA_list = [ETA1, ETA2, msg1, msg2]

    return ETA_list

if __name__ == "__main__":
    update_busarr()