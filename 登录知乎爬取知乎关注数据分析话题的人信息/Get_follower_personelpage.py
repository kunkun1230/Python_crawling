# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 22:57:22 2017

@author: lenovo
"""

import urllib.request
import requests
import random
import time
import os
import os.path
from bs4 import BeautifulSoup
try:
    import cookielib
except:
    import http.cookiejar as cookielib
from PIL import Image

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection': 'keep-alive',
    'Cookie':'q_c1=9d9d5459de7c4b39be34961f587d1b93|1506611544000|1506611544000; d_c0="AABC35tWcgyPTnzFfYhQnseM1HqmAEJ233Q=|1506611544"; _zap=9b27e9ae-9d20-4c12-9e94-51d654def9e8; _xsrf=1bd1b07f61441f3d68c804319abd8ef8; aliyungf_tc=AQAAALjRvjOHBgcADwbOt3CLW2lIpObj; _xsrf=1bd1b07f61441f3d68c804319abd8ef8; r_cap_id="OGMzMjBhOWFjYWFkNDUxNWFiMmEwNDI1MDMxNDllODg=|1508513276|46ec8ade00c07e04196452b9646311f11740c53b"; cap_id="ZmQwMjgxZWE4MGYzNDZlZjg5ODBlYmZkZDZlYTQwODA=|1508513276|af0d450c09b8b9656a3542ad2d968e3179b33d09"; __utma=51854390.1342851571.1506611545.1508504130.1508513278.5; __utmb=51854390.0.10.1508513278; __utmc=51854390; __utmz=51854390.1508504130.4.4.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.000--|2=registration_date=20151218=1^3=entry_date=20170928=1; z_c0=Mi4xaXNCakFnQUFBQUFBQUVMZm0xWnlEQmNBQUFCaEFsVk5EMlRYV2dBUzU0Wjl6RlF5c1VEOFhwVHFoSV9OQWlqWXV3|1508513295|2d1b1bf20ca71b4a706a05454ad495f7f7196021',
    'Host': 'www.zhihu.com',
    'Referer':'https://www.zhihu.com/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36',
}#这里如果一开始就出现302的错误，需替换最新的Cookie

HostUrl = 'http://www.zhihu.com'
FollowerUrl = 'https://www.zhihu.com/topic/19559424/followers' #关注数据分析的关注者页面
LoginUrl = 'https://www.zhihu.com/login/email'
timeout = random.choice(range(60, 180))
session = requests.session()

#使用cookie信息加载
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)  #ignore_discard的意思是即使cookies将被丢弃也将它保存下来
except:
    print("cookie加载失败")

def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url,allow_redirects=False,headers = headers).status_code
    print(login_code)
    if int(x=login_code) == 200:
        return True
    else:
        return False

#验证登录
def login(url):
    login_data = {
        '_xsrf' : get_xsrf(url),
        'password' : '*********',
        'remember_me' : 'true',
        'email' : '********@163.com'
    }
    try:#不需要验证码登录
        repr=session.post(LoginUrl, data=login_data, headers=headers)
        print(repr)
    except:#需要验证码登录
        login_data['captcha_type'] = 'cn'
        login_data['captcha'] = get_captcha()
        repr = session.post(LoginUrl,data=login_data,headers=headers)
        print(repr)
    session.cookies.save()

#获取_xsrf
def get_xsrf(url):
    res = session.get(url,headers = headers,timeout=timeout).content
    _xsrf = BeautifulSoup(res,'html.parser').find('input',attrs={'name':'_xsrf'})['value']
    print(_xsrf)
    return _xsrf

#解析验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha

#加载页面获取html内容，主要offset
def get_html():
    url = FollowerUrl
    res = session.get(url,headers=headers)#进入数据分析话题
    _xsrf = BeautifulSoup(res.content,'html.parser').find('input',attrs={'name':'_xsrf'})['value']
    with open('follower_link1.txt','w',encoding='utf-8') as f:
        name_list=getUrl(res.text)
        for i in name_list:
            f.write(str(i))
    time.sleep(random.choice(range(2,5)))
    print(_xsrf)
    
    headers1={
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Content-Length':'17',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie':'q_c1=9d9d5459de7c4b39be34961f587d1b93|1506611544000|1506611544000; d_c0="AABC35tWcgyPTnzFfYhQnseM1HqmAEJ233Q=|1506611544"; _zap=9b27e9ae-9d20-4c12-9e94-51d654def9e8; _xsrf=1bd1b07f61441f3d68c804319abd8ef8; aliyungf_tc=AQAAALjRvjOHBgcADwbOt3CLW2lIpObj; r_cap_id="OGMzMjBhOWFjYWFkNDUxNWFiMmEwNDI1MDMxNDllODg=|1508513276|46ec8ade00c07e04196452b9646311f11740c53b"; cap_id="ZmQwMjgxZWE4MGYzNDZlZjg5ODBlYmZkZDZlYTQwODA=|1508513276|af0d450c09b8b9656a3542ad2d968e3179b33d09"; z_c0=Mi4xaXNCakFnQUFBQUFBQUVMZm0xWnlEQmNBQUFCaEFsVk5EMlRYV2dBUzU0Wjl6RlF5c1VEOFhwVHFoSV9OQWlqWXV3|1508513295|2d1b1bf20ca71b4a706a05454ad495f7f7196021; _xsrf=1bd1b07f61441f3d68c804319abd8ef8; __utma=51854390.1342851571.1506611545.1508504130.1508513278.5; __utmb=51854390.0.10.1508513278; __utmc=51854390; __utmz=51854390.1508504130.4.4.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20151218=1^3=entry_date=20151218=1',
            'Host':'www.zhihu.com',
            'Origin':'https://www.zhihu.com',
            'Referer':'https://www.zhihu.com/topic/19559424/followers',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            }
    
    headers1['X-Xsrftoken'] = _xsrf
    
    with open('follower_link1.txt','a',encoding='utf-8') as f1:
        for x in range(20,4000000,20):
            form_data = {
                'start' : '0',
                'offset' : str(x),
                '_xsrf' : _xsrf
            }
            print(str(x))
            try:
                res= session.post(url,data=form_data,headers=headers1)
                print(res)
            except:
                print("offset加载失败")
            else:
                content = res.text
                html = eval(content)['msg'][1] #用文件保存这个链接，发现里面的标签里面多了'\\'，为了不影响后期soup读取网页，先替换掉
                html = str(html).replace('\\','')
                getUrl(html)
                for i in getUrl(html):
                    f1.write(i)
        time.sleep(random.choice(range(1,5)))

#根据content内容提取头像
def getUrl(content):
    followers = []
    bs4 = BeautifulSoup(content, "html.parser")
    users = bs4.find_all(class_='zm-list-content-title')#查找所有关注者
    for user in users:
        temp = []
        username = user.find('a').string  #查找关注者姓名 class=\"zg-link author-link\"
        followerUrl = user.find('a').get('href') #查找用户头像url
        link=str(followerUrl).replace('\\','')
        followerUrl = 'https://www.zhihu.com'+link
        temp=username+','+followerUrl+'\n'
        print(temp)
        followers.append(temp)
    return followers

if __name__ == '__main__':
    if isLogin():
        print("已经登录")
    else:
        print("重新登录")
        login(HostUrl)
    _xsrf = get_xsrf(HostUrl) #粉丝页的xsrf和首页是不一样的
    #_xsrf = get_xsrf(FollowerUrl)
    get_html()
