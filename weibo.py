#encoding=utf-8
import requests
import json
import base64
from bs4 import BeautifulSoup
import sys
import time
import traceback
reload(sys)
sys.setdefaultencoding('utf-8')

fname = 'data/weibo.txt'

QT = [
    {'url':'http://s.weibo.com/top/summary?cate=realtimehot','s1':'实时热搜榜'},
]

def get_all_item():
    try:
        s = requests.Session()
        for u in QT:
            url = u['url']
            r = s.get(url)
            print(r.status_code)
            soup = BeautifulSoup(r.text)
            #print(soup.prettify())
            s = soup.find_all('script')[-2].string

            td01_1 = s.index('td_01') - 10
            td01_2 = s.index('td_01', td01_1+1) -10
            print(td01_1)
            print(td01_2)
            print(s[td01_1:td01_2])


    except Exception as e:
        err = traceback.format_exc()
        print(err)

if __name__ == '__main__':

    try:
        get_all_item()
        pass
    except Exception as e:
        err = traceback.format_exc()
        print(err)
