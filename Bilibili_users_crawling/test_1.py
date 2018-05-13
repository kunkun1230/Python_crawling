# -*- coding: utf-8 -*-
# 自己造的轮子

"""
Created on Mon Apr 16 15:36:27 2018

@author: lenovo
"""

import chardet #识别网页写入语言的模块

import requests
import json
import random

import sys
import datetime
import time
from imp import reload

import psycopg2   #导入pymysql 输入到PostgreSQL中
from multiprocessing.dummy import Pool as ThreadPool

url='https://space.bilibili.com/ajax/member/GetInfo'

#---------------------构建请求头-----------------------------------------------
head={'Accept':'application/json, text/plain, */*',
      'Accept-Encoding':'gzip, deflate, br',
      'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
      'Cache-Control':'max-age=0',
      'Connection':'keep-alive',
      'Content-Length':'51',
      'Content-Type':'application/x-www-form-urlencoded',
      'Cookies':'finger=964b42c0; buvid3=817EE659-7A25-48CF-AD44-58F92011840A24927infoc; fts=1523863333; UM_distinctid=162cd5529e41211-020bde6a248812-4c322073-144000-162cd5529e611cc; CNZZDATA2724999=cnzz_eid%3D702428954-1523859402-%26ntime%3D1523859402; sid=jmscumbh; DedeUserID=316371558; DedeUserID__ckMd5=9fcf566cc5df8474; SESSDATA=dfd60d9d%2C1526455496%2C6a70e6eb; bili_jct=53199b613530c66840c7445852819641; _dfcaptcha=f7ce8033c220c1fad645143b0185ded0; LIVE_BUVID=AUTO8715238634997765',
      'Host':'space.bilibili.com',
      'Referer':'https://space.bilibili.com/10000',
      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
      }

#------------------建立时间戳，这个意义我目前还没看懂---------------------------
def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))

    return current_milli_time()

#-----------------------建立U-A池子--------------------------------------------
def LoadUserAgents(uafile):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-2])
    random.shuffle(uas) #对所有用到的UA进行重新洗牌
    return uas

uas = LoadUserAgents(r'C:\Users\lenovo\Desktop\bilibili-user-master\bilibili-user-master\user_agents.txt')


#----------------------构建代理------------------------------------------------这里我是在无忧代理上买的

url1='http://api.ip.data5u.com/dynamic/get.html?order=7a8605c9cc612019e9d3bd7a3163723f&sep=3'

def getproxies(url1):
    b=requests.get(url1).content
    proxies={'http':str(b)[2:-3]}
    print(proxies)
    return proxies

#----------------------读取网页内容，并提取数据---------------------------------------
def getsource(url):
        payload = {
            '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
            'mid': url.replace('https://space.bilibili.com/', '')     #编辑网页post的参数
        }
        ua = random.choice(uas)
        head = {
            'User-Agent': ua,
            'Referer': 'https://space.bilibili.com/' + str(i) + '?from=search&seid=' + str(random.randint(10000, 50000))
        } #添加请求头里的UA和Referer数据
        
        jscontent = requests\
                    .session()\
                    .post('http://space.bilibili.com/ajax/member/GetInfo',\
                     headers=head,data=payload,proxies=proxies).content #发送请求获取内容
        
        
        time2 = time.time()
        
        #处理获取后的网络数据
        try:
            jsDict = json.loads(jscontent)
            statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
            if statusJson == True:
                if 'data' in jsDict.keys():
                    jsData = jsDict['data']
                    mid = jsData['mid']
                    name = jsData['name']
                    sex = jsData['sex']
                    face = jsData['face']
                    coins = jsData['coins']
                    spacesta = jsData['spacesta']
                    birthday = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                    place = jsData['place'] if 'place' in jsData.keys() else 'noplace'
                    description = jsData['description'] if 'description' in jsData.keys() else 'nodescription'
                    article = jsData['article'] if 'article' in jsData.keys() else 'noarticle'
                    playnum = jsData['playNum'] if 'playNum' in jsData.keys() else 'noplayNum'
                    sign = jsData['sign'] 
                    if "'" not in sign:    # 之所以写这个的原因是因为发现写入PostgreSQL时，由于字符串中存在',出现了ProgrammingError: syntax error at or near的错误
                        sign=sign
                    else:
                        sign=sign.replace("'","''")
                    level = jsData['level_info']['current_level']
                    exp = jsData['level_info']['current_exp'] if 'current_exp' in jsData['level_info'].keys() else 'noexp'
                    print("Succeed: " + str('%s')%(mid) + "\t" + str(time2 - time1))
                    try:
                        res = requests.get(
                            'https://api.bilibili.com/x/relation/stat?vmid=' + str(mid) + '&jsonp=jsonp').text  #关注者和粉丝数量并不与上面的信息在同一个请求中，因此要额外请求一次
                        js_fans_data = json.loads(res)
                        following = js_fans_data['data']['following']
                        fans = js_fans_data['data']['follower']
                    except:
                        following = 0
                        fans = 0
                else:
                    print('no data now')
                try:                               # PostgreSQL中的数据必须用单引号来引用，如果用双引号就会出现错误
                    cur.execute("INSERT INTO bilibili_user_info1(mid, name, sex, face, coins, spacesta, \
                    birthday, place, description, article, following, fans, playnum, sign, level, exp) \
                    VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"% (mid, name, sex, face, coins, spacesta,birthday, place, description, article,following, fans, playnum,sign, level, exp))
                    conn.commit()    #先去掉在level之前的sign看看怎么样
                except Exception as err:
                    print("PostgreSQL Error"+'\t'+repr(err)) #如果这里出错，那么是数据库的错
                    #conn.close() # 因为数据库在一直输入的过程中，如果前一个出了错误，那么后面所有的都会提示错误，所以这里比较明智的方式是关闭一次，再重新开启，确保出错的数据量最小
                    #conn = psycopg2.connect(database="123", user="postgres", password="123456", host="127.0.0.1", port="5432") #host这个地方默认写"127.0.0.1"就好
                    #conn.cursor()
            else:
                print("Error: " + url)
        except ValueError as err: #这里应该是网页错误了
            print(str('Web question \t')+repr(err))
            pass
        global url2
        url2=url
    
def updateurls(url):
    n=urls.index(url)
    url3=urls[(n+1):]
    return url3


time1 = time.time() #记录开始时间

pool = ThreadPool(1)
conn = psycopg2.connect(database="123", user="postgres", password="123456", host="127.0.0.1", port="5432") #host这个地方默认写"127.0.0.1"就好
print('数据库开启成功')
point1=time.time()
cur=conn.cursor()

url2=''

for m in range(6, 101):  # 1 ,101 #获取用户的个人网页信息
    urls = []
    for i in range(m * 100, (m + 1) * 100):
        url = 'https://space.bilibili.com/' + str(i)
        urls.append(url)

    try:
        #写入代理
        proxies=getproxies(url1)
        results = pool.map(getsource, urls)
    except Exception as err:
        print(repr(err))
        print('ConnectionError') 
        print('更换代理ip')
        pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
        pool.join()   # 等待进程池中的所有进程执行完毕  ？？？
        time.sleep(5)
        pool = ThreadPool(1)
        urls=updateurls(url2)
        proxies=getproxies(url1) #更换代理
        results = pool.map(getsource, urls)

    time.sleep(30)

pool.close()
pool.join()

