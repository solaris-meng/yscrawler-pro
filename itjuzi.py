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
        for i in range(1, 2):
            url = 'https://www.itjuzi.com/investevents?page=%d' % i
            r = s.get(url)
            print(r.status_code)
            soup = BeautifulSoup(r.text)
            lis = soup.find_all('ul', 'list-main-eventset')[1]
            for li in lis.find_all('li'):
                dt = li.find('i', 'cell round').find('span').string.strip()
                url = li.find('i', 'cell pic').find('a').attrs['href'].strip()
                name = li.find_all('p')[0].find('a').find('span').string
                cat = li.find_all('p')[1].find_all('span')[0].find('a').string.strip()
                location = li.find_all('p')[1].find_all('span')[1].find('a').string.strip()
                rd = li.find_all('i', 'cell round')[1].find('a').find('span').string.strip()
                fina = li.find('i', 'cell fina').string

                print(dt)
                #print(url)
                print(name)
                #print(cat)
                #print(location)
                #print(rd)
                #print(fina)
                item = {}
                item['key'] = '%s %s' % (dt, name)
                item['dt'] = url
                item['url'] = url
                item['name'] = name
                item['cat'] = cat
                item['location'] = location
                item['rd'] = rd
                item['fina'] = fina
                item['des'] = get_des(url)

                url = 'http://meng.wiki/crawler/Itjuzi/'
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

