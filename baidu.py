#encoding=utf-8
import requests
import json
import base64
from bs4 import BeautifulSoup
import sys
import time
import datetime
import hashlib
import traceback
reload(sys)
sys.setdefaultencoding('utf-8')

fname = 'data/baidu.txt'

INDEX = 0
INDEX = 1

QT = [
    {'url':'http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b342_c513','s1':'实时热点'},
    {'url':'http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b1_c513','s1':'今日热点'},
    {'url':'http://top.baidu.com/buzz?b=42&c=513','s1':'七日热点'},
    {'url':'http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b42_c513','s1':'民生热点'},
    {'url':'http://top.baidu.com/buzz?b=344&c=513','s1':'娱乐热点'},
    {'url':'http://top.baidu.com/buzz?b=11&c=513&fr=topbuzz_b344_c513','s1':'体育热点'},
]

def save_to_ys(i):
    try:
        url = 'http://127.0.0.1:7008/crawler/Baidutop/'
        r = requests.post(url, auth=('admin', 'brotec666'), json=i)
        return '%d' % r.status_code
    except Exception as e:
        err = traceback.format_exc()
        print(err)
        return err
    return 'failed'
def get_all_item():
    try:
        session = requests.Session()
        for u in QT:
            url = u['url']
            s1 = u['s1']

            r = session.get(url)
            r.encoding = 'gb2312'
            print(r.status_code)
            print(r.encoding)
            soup = BeautifulSoup(r.text)
            #print(soup.prettify())

            s = soup.find_all('tr')

            count = 1
            for tr in s:
                if count > 50:
                    break
                td = tr.get_text().split()
                if td[0].isdigit():
                    i = {}
                    i['rank'] = td[0]
                    i['word'] = td[1]
                    i['s1'] = s1
                    i['date_str'] = datetime.datetime.today().strftime('%Y-%m-%d')
                    uuid_str = i['date_str']+i['s1']+i['rank']
                    i['uuid'] = hashlib.sha1(uuid_str.encode('utf-8')).hexdigest()

                    r = ''
                    r = save_to_ys(i)
                    print(i['date_str']+' '+i['s1']+' '+i['rank']+' '+i['word']+' '+r)

                count += 1


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
