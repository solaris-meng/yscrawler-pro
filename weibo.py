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

            start = 0
            while True:
                try:
                    td01_1 = s.index('td_01', start) - 12
                    td01_2 = s.index('td_01', td01_1+13) - 55
                except ValueError:
                    break
                item = s[td01_1:td01_2]

                soup_item = BeautifulSoup(item)
                #print(soup_item.prettify())
                item= soup_item.get_text().replace('\\n', '').split()
                print(item)
                rank = item[0]
                word = item[1]
                value = item[2]
                #rank = item[0].rtrip('\\n')
                #word = item[1].rtrip('\\n')
                #value = item[2].rtrip('\\n')
                print(rank)
                print(word.decode('unicode-escape'))
                print(value)

                start = td01_2


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
