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

fname = 'data/weibo.txt'

INDEX = 0
INDEX = 1

QT = [
    {'url':'http://s.weibo.com/top/summary?cate=realtimehot','s1':'实时热搜榜'},
    {'url':'http://s.weibo.com/top/summary?cate=total&key=friends','s1':'好友热搜榜'},
    {'url':'http://s.weibo.com/top/summary?cate=total&key=all','s1':'热点热搜榜'},
    {'url':'http://s.weibo.com/top/summary?cate=total&key=films','s1':'潮流热搜榜'},
    {'url':'http://s.weibo.com/top/summary?cate=total&key=person','s1':'名人热搜榜'},
]

def save_to_ys(i):
    try:
        url = 'http://101.200.130.178/crawler/Weibotop/'
        r = requests.post(url, auth=('admin', 'brotec'), json=i)
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
            print(r.status_code)
            soup = BeautifulSoup(r.text)
            #print(soup.prettify())
            s = soup.find_all('script')[-2].string

            start = 0
            rank = 1
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
                #print(item)
                word = item[1]

                i = {}
                i['rank'] = '%d' % rank
                i['word'] = word.decode('unicode-escape').replace('-->','')
                i['s1'] = s1
                i['date_str'] = datetime.datetime.today().strftime('%Y-%m-%d')
                uuid_str = i['date_str']+i['s1']+i['rank']
                i['uuid'] = hashlib.sha1(uuid_str.encode('utf-8')).hexdigest()

                r = ''
                #r = save_to_ys(i)
                print(i['date_str']+' '+i['s1']+' '+i['rank']+' '+i['word']+' '+r)
                #rank = item[0].rtrip('\\n')
                #word = item[1].rtrip('\\n')
                #value = item[2].rtrip('\\n')
                #print(word.decode('unicode-escape'))

                rank += 1
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
