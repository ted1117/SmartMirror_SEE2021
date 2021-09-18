"""
연합뉴스에서 제공하는 헤드라인 RSS를 이용하여 오늘의 헤드라인 수집
"""

import requests
import xmltodict # 따로 설치
import json

def get_newsfeed():
    """
    연합뉴스 rss에서 헤드라인을 수집하여 리스트에 추가

    제공되는 헤드라인 5개가 포함된 리스트 news_headline이 리턴됨
    """
    url = "https://www.yonhapnewstv.co.kr/category/news/headline/feed/" # 연합뉴스 헤드라인 RSS 이용
    res = requests.get(url)
    xml = xmltodict.parse(res.text)
    dict1 = json.loads(json.dumps(xml))
    dict_data = dict1["rss"]["channel"]["item"]

    # 헤드라인 리스트 생성
    news_headlines = []
    
    # 리스트에 헤드라인 추가
    for n in range(len(dict_data)):
        news_headlines.append(dict_data[n]['title'])

    return news_headlines
    
if __name__ == "__main__":
    get_newsfeed()