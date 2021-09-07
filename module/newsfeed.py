# -*- coding: utf-8 -*-
import requests
import xmltodict # 따로 설치
import json
import time

def get_newsfeed():
    url = "https://www.yonhapnewstv.co.kr/category/news/headline/feed/"
    res = requests.get(url)
    xml = xmltodict.parse(res.text)
    dict1 = json.loads(json.dumps(xml))
    #print(dict1['rss']['channel']['item'][0])
    dict_data = dict1["rss"]["channel"]["item"]
    news_headlines = []
    
    for n in range(len(dict_data)):
        news_headlines.append(dict_data[n]['title'])

    return news_headlines
    
if __name__ == "__main__":
    a = get_newsfeed()
    print(a)