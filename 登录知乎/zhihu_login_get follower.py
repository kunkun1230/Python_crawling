# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 23:05:07 2017

@author: lenovo
"""

'''
Required
- requests (必须)
- pillow (可选)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.2.4"
Update
- name   : "wangmengcn"
- email  : "eclipse_sv@163.com"
- date   : "2016.4.21"
'''
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass
from bs4 import BeautifulSoup as bs

#--------------------------------以下是登陆代码----------------------------------------
# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_xsrf():
    logn_url = 'http://www.zhihu.com/#signin'
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'
    }
    content = session.get(logn_url, headers=headers).content
    soup = bs(content, 'html.parser')
    print(soup.find('input', attrs={'name': "_xsrf"})['value'])
    return soup.find('input', attrs={'name': "_xsrf"})['value']


# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
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


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


def login(secret, account):
    _xsrf = get_xsrf()
    headers["X-Xsrftoken"] = _xsrf
    headers["X-Requested-With"] = "XMLHttpRequest"
    # 通过输入的用户名判断是否是手机号
    if re.match(r"^1\d{10}$", account):
        print("手机号登录 \n")
        post_url = 'https://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': _xsrf,
            'password': 31415926,
            'phone_num': '18007177686'
        }
    else:
        if "@" in account:
            print("邮箱登录 \n")
        else:
            print("你的账号输入有问题，请重新登录")
            return 0
        post_url = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': _xsrf,
            'password': 31415926,
            'email': 'chengkun1230@163.com'
        }
    # 不需要验证码直接登录成功
    login_page = session.post(post_url, data=postdata, headers=headers)
    login_code = login_page.json()
    if login_code['r'] == 1:
        # 不输入验证码登录失败
        # 使用需要输入验证码的方式登录
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.json()
        print(login_code['msg'])
    # 保存 cookies 到文件，
    # 下次可以使用 cookie 直接登录，不需要输入账号和密码
    session.cookies.save()

try:
    input = raw_input
except:
    pass

#------------------------------------这是获取数据的代码-----------------------
def getdetail():
    follower_url='https://www.zhihu.com/people/kunkun_1230/followers'
    follower_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Referer': 'https://www.zhihu.com/people/kunkun_1230/followers',
        'Origin': 'https://www.zhihu.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*'}
    m_data={'_xsrf':str(get_xsrf())}
    result = session.post(follower_url, data=m_data, headers=follower_headers)
    soup=bs(result.content,'lxml')
    with open('soup','w',encoding='utf-8') as f:
        f.write(str(soup))

#----------------------------------这是粘合剂-------------------------
if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
    else:
        account = input('请输入你的用户名\n>  ')
        secret = input("请输入你的密码\n>  ")
        login(secret, account)
    get_xsrf()
    getdetail()
