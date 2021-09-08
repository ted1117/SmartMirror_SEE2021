import requests
import xmltodict # 따로 설치
import json

def get_newsfeed():
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
    a = get_newsfeed()
    print(a)