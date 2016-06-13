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

def get_des(url):
    try:
        s = requests.Session()
        r = s.get(url)
        soup = BeautifulSoup(r.text)
        lis = soup.find_all('p')
        des = lis[8].text
        return des
    except Exception as e:
        return 'failed'

def get_all_item():
    try:
        s = requests.Session()
        url = 'http://next.36kr.com/posts'
        r = s.get(url)
        soup = BeautifulSoup(r.text)
        #print(soup.prettify())
        lis = soup.find_all('li',"item product-item ")

        for i in lis:
            print(i.find('a', "post-url").text)
            print(i.find('a', "post-url")['href'])
            print(i.find('span', "post-tagline").text)
            print(i.find('span', "vote-count").text)

            item = {}
            item['url'] = i.find('a', "post-url")['href']
            item['name'] = i.find('a', "post-url").text
            item['des'] = i.find('span', "post-tagline").text
            item['vote'] = i.find('span', "vote-count").text

            url = 'http://meng.wiki/crawler/Krnext/'
            r = requests.post(url, auth=('admin', 'anmeng88'), json=item)
            status_code = r.status_code
            print('%d' % status_code)

    except Exception as e:
        err = traceback.format_exc()
        print(err)
    #get_user_info(5880199981, session)
    #print(json.dumps(fans_tmp3,sort_keys=True,indent=4, separators=(',', ': ')))

if __name__ == '__main__':

    try:
        get_all_item()
        #get_des('https://www.itjuzi.com/investevents/17625')
        pass
    except Exception as e:
        err = traceback.format_exc()
        print(err)
    #get_user_info(5880199981, session)
    #print(json.dumps(fans_tmp3,sort_keys=True,indent=4, separators=(',', ': ')))

