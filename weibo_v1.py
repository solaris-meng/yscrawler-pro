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

USERNAME = 'moushi_yushan@sina.com'
PASSWORD = 'yushan_admin'

# 方法1: 批量获取粉丝信息
# 原理: - 根据UID获取该用户的前20页的粉丝信息，包括昵称，年龄，地区，UID等信息
#       - 根据上一步获取的大概200个粉丝，递归获取这200个粉丝的前20页粉丝信息
#       - 因为weibo.cn的查看粉丝页面总共只显示20页
#
# 例如，高晓松的UID为1191220232
FANS_START = '1191220232'
# 一共采集的粉丝的总数量
FANS_TOTAL = 100
# 对每个用户采集多少页的粉丝, 最大为20页
FANS_PER_USER = 1


def login(username, password):
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    session = requests.Session()
    res = session.post(loginURL, data = postData)
    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        print("登录成功")
        # 把cookies添加到headers中，必须写这一步，否则后面调用API失败
        cookies = session.cookies.get_dict()
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)
        session.headers["cookie"] = cookies
        #session.headers["User-agent"] = {'User-agent': 'spider'}
    else:
        print("登录失败，原因： %s" % info["reason"])
    return session

def get_user_info(uid, session):
    url = "http://weibo.cn/%s/info" % uid
    r = session.get(url)
    soup = BeautifulSoup(r.text)
    #print(soup.prettify())

    sex = 'init'
    location = 'init'
    marry = 'init'
    info = 'init'

    infos = soup.find_all('div')
    if len(infos) < 5:
        return sex,location,marry,info

    info = infos[4].prettify().split()
    for i in info:
        tk = i.split(':')
        if len(tk) < 2:
            continue

        if tk[0] == '性别':
            sex = tk[1]
        if tk[0] == '地区':
            location = tk[1]
        if tk[0] == '感情状况':
            marry = tk[1]
    return sex,location,marry,infos[4].get_text()

def get_fans(uid, session, total, filename):
    if total > FANS_TOTAL:
        return 0

    total += 1

    fd = open(filename, 'a+')
    url="http://weibo.cn/%s/fans" % uid

    r = session.get(url)
    soup = BeautifulSoup(r.text)

    # for debug
    #print(soup.prettify())

    # get total pages
    count = 20

    # parse all fans
    l = []
    for i in range(1,FANS_PER_USER):
        i += 1
        r = session.get(url)
        soup = BeautifulSoup(r.text)
        for t in soup.find_all('table'):
            u_url = t.tr.find_all('td')[0].a['href']
            u_name = t.tr.find_all('td')[1].a.string
            u_num_fan = t.tr.find_all('td')[1].get_text().split('粉丝')[1].split('人')[0]
            u_pic = t.tr.td.a.img['src']

            u_id = u_url.split('/')[-1]
            sex,location,marry,info = get_user_info(u_id, session)
            line = u_id+' '
            line += u_url+' '
            line +=u_name+' '
            line +=u_num_fan+' '
            line +=sex+' '
            line +=location+' '
            line +=marry+' '
            line +=u_pic+' '
            line +='/%s/' % info+' '
            fd.write(line+'\n')
            l.append(u_id)
    fd.close()

    for i in l:
        get_fans(i, session, total, filename)

if __name__ == '__main__':
    session = login(USERNAME, PASSWORD)

    try:
        filename = FANS_START+'.fans'
        get_fans(FANS_START, session, 1, filename)
    except Exception as e:
        err = traceback.format_exc()
        print(err)
    #get_user_info(5880199981, session)
    #print(json.dumps(fans_tmp3,sort_keys=True,indent=4, separators=(',', ': ')))

