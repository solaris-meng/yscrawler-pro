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
from PIL import Image
from StringIO import StringIO
reload(sys)
sys.setdefaultencoding('utf-8')

fname = 'data/baidu.txt'


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

        url = "http://cn.bing.com/"
        r = session.get(url)
        r.encoding = 'utf-8'
        print(r.status_code)
        print(r.encoding)
        #soup = BeautifulSoup(r.text)
        #print(soup.prettify())
        raw = r.text
        start = 0
        urls = []
        while True:
            try:
                idx = raw.index('url', start)
                print(raw[idx:idx+100])
                urls.append(raw[idx:idx+100])
                start = idx+20
            except Exception as e:
                break
        bg_url = urls[-5].split('"')[1].replace('\\','')
        print(bg_url)
        date_str = datetime.datetime.today().strftime('%Y-%m-%d')
        filename = '/Users/mengan/test/yscrawler_pro/bing/%s.jpg' % date_str
        bg_raw = requests.get(bg_url)
        bg_file = Image.open(StringIO(bg_raw.content))
        bg_file.save(filename)

        with open('/tmp/bing.log','a+') as fd:
            fd.write(date_str+'\n')

    except Exception as e:
        err = traceback.format_exc()
        print(err)

if __name__ == '__main__':

    try:
        pics = []
        try:
            f = open("/tmp/bing.log", 'r')
            for line in f:
                pics.append(line.strip('\n'))
        except Exception as e:
            pass

        date_str = datetime.datetime.today().strftime('%Y-%m-%d')
        if date_str not in pics:
            get_all_item()
        else:
            print('done '+date_str)
            pass
    except Exception as e:
        err = traceback.format_exc()
        print(err)
