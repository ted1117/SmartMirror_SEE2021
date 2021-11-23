import requests
import urllib.parse
import datetime
import xmltodict # 따로 설치
import json

def getDCDcnt():
    with open("secret.json") as json_file:
        json_data = json.load(json_file)

    url = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson"
    service_key = json_data

    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")
    yesterday_tmp = now - datetime.timedelta(days=1)
    yesterday = yesterday_tmp.strftime("%Y%m%d")

    queryParams = "?" + urllib.parse.urlencode({
                        urllib.parse.quote_plus("serviceKey"): urllib.parse.unquote(service_key),
                        urllib.parse.quote_plus("pageNo"): "1",
                        urllib.parse.quote_plus("numOfRows"): "10",
                        urllib.parse.quote_plus("startCreateDt"): yesterday,
                        urllib.parse.quote_plus("endCreateDt"): today,
                    })

    res = requests.get(url + queryParams)
    print(url + queryParams)
    xml = xmltodict.parse(res.text)
    dict1 = json.loads(json.dumps(xml))
    dict_data = dict1['response']['body']['items']['item']

    decide_cnt = int(dict_data[0]["decideCnt"]) - int(dict_data[1]["decideCnt"])
    
    return decide_cnt

if __name__ == "__main__":
    getDCDcnt()