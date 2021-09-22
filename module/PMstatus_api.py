import requests
import urllib.parse
import datetime
import xmltodict # 따로 설치
import json

def getPMstatus():
    with open("secret.json") as json_file:
        json_data = json.load(json_file)

    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
    service_key = json_data

    # 측정소 위치
    stn_site = "동작구"

    queryParams = "?" + urllib.parse.urlencode({
                        urllib.parse.quote_plus("serviceKey"): urllib.parse.unquote(service_key),
                        urllib.parse.quote_plus("returnTypereturnType"): "xml",
                        urllib.parse.quote_plus("numOfRows"): "100",
                        urllib.parse.quote_plus("pageNo"): "1",
                        urllib.parse.quote_plus("stationName"): stn_site,
                        urllib.parse.quote_plus("dataTerm"): "DAILY",
                        urllib.parse.quote_plus("ver"): "1.3"
                    })


    res = requests.get(url + queryParams)
    xml = xmltodict.parse(res.text)
    dict1 = json.loads(json.dumps(xml))
    PM_dict = dict1['response']['body']['items']['item'][0]

    return PM_dict


if __name__ == "__main__":
    print(getPMstatus())