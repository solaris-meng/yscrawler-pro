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

fname = 'data/itjuzi.txt'

def get_all_item():
    try:
        s = requests.Session()
        for i in range(1, 1322):
            url = 'https://www.itjuzi.com/investevents?page=%d' % i
            r = s.get(url)
            print(r.status_code)
            soup = BeautifulSoup(r.text)
            lis = soup.find_all('ul', 'list-main-eventset')[1]
            for li in lis.find_all('li'):
                dt = li.find('i', 'cell round').find('span').string
                url = li.find('i', 'cell pic').find('a').attrs['href']
                name = li.find_all('p')[0].find('a').find('span').string
                cat = li.find_all('p')[1].find_all('span')[0].find('a').string
                location = li.find_all('p')[1].find_all('span')[1].find('a').string
                rd = li.find_all('i', 'cell round')[1].find('a').find('span').string
                fina = li.find('i', 'cell fina').string

                print(dt)
                print(url)
                print(name)
                print(cat)
                print(location)
                print(rd)
                print(fina)
                if True:
                    line = ''
                    line += dt+'\t'
                    line += url+'\t'
                    line += name+'\t'
                    line += cat+'\t'
                    line += location+'\t'
                    line += rd+'\t'
                    line += fina.strip()+'\t'
                    with open(fname, 'a+') as fd:
                        fd.write(line+'\n')

    except Exception as e:
        err = traceback.format_exc()
        print(err)
    #get_user_info(5880199981, session)
    #print(json.dumps(fans_tmp3,sort_keys=True,indent=4, separators=(',', ': ')))

if __name__ == '__main__':

    try:
        get_all_item()
        pass
    except Exception as e:
        err = traceback.format_exc()
        print(err)
    #get_user_info(5880199981, session)
    #print(json.dumps(fans_tmp3,sort_keys=True,indent=4, separators=(',', ': ')))

