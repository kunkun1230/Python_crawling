# -*- coding: utf-8 -*-
"""
Created on Sat May 19 14:32:31 2018

@author: lenovo
"""

import requests
import base64
import time
import json
import re
import hashlib
import hmac
from http import cookiejar
from PIL import Image             #用于打开图片验证码
import matplotlib.pyplot as plt   #用于识别文字验证码，并返回倒着的文字坐标

'''
列出需要post的参数
'''

login_data={'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type':'password',
            'source':'com.zhihu.web',
            'signature':'',
            'username':'',
            'password':'',
            'captcha':'',
            'lang':'en',
            'timestamp':'',
            }

headers={'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
         'Connection':'keep-alive',
         'Host':'www.zhihu.com',
         'Referer':'https://www.zhihu.com/signup',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',	
         }

u_a={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}

login_url='https://www.zhihu.com/signup'

login_api='https://www.zhihu.com/api/v3/oauth/sign_in'

session=requests.session()
session.cookies=cookiejar.LWPCookieJar('./cookies.txt')
session.headers=headers


def login(login_url):
    if load_cookies():
        if check_login():
            return True
    
    headers.update({'x-xsrftoken':get_token(login_url)}) #实时更新x-xsrftoken信息，这是后期通过headers获取验证码的关键
    
    check_user_pass(login_data)   #测试登录账户密码
    
    login_data.update({'signature':get_signature(timestamp),
                       'timestamp':str(timestamp),
                       'captcha':get_captcha(headers)
                       })
    
    resp=session.post(login_api,data=login_data,headers=headers)
    
    if 'error' in resp.text:
            print(re.findall(r'"message":"(.+?)"', resp.text)[0])
    elif check_login():
            return True
    else:
            print('登录失败')
            return False
    
    
def load_cookies():
    '''
    查看当前文件夹中是否已有cookies文件
    '''
    try:
        session.cookies.load(ignore_discard=True) #ignore_discard的意思是即使cookies将被丢弃也将它保存下来，ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
        return True
    except FileNotFoundError:
        return False

def check_login():
    '''
    检查网页登录情况
    '''
    resp=session.get(login_url, allow_redirects=False) 
    if resp.status_code == 302:
        print('登录成功')
        session.cookies.save()
        return True
    else:
        print('登录失败')
        return False

def get_captcha(headers):
        """
        请求验证码的 API 接口，无论是否需要验证码都需要请求一次
        如果需要验证码会返回图片的 base64 编码
        根据头部 lang 字段匹配验证码，需要人工输入
        :param headers: 带授权信息的请求头部
        :return: 验证码的 POST 参数
        一般都是在第一次运行的时候会出现验证码，并且一般是英文的
        """
        lang = headers.get('lang', 'en')
        if lang == 'cn':
            api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
        else:
            api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        resp = session.get(api, headers=headers)
        show_captcha = re.search(r'true', resp.text)
        if show_captcha:
            put_resp = session.put(api, headers=headers)
            #print('put_resp'+str(put_resp))  #显示api的内容
            img_base64 = re.findall(
                r'"img_base64":"(.+)"', put_resp.text, re.S)[0].replace(r'\n', '')
            with open('./captcha.jpg', 'wb') as f:
                f.write(base64.b64decode(img_base64))
            img = Image.open('./captcha.jpg')
            if lang == 'cn':
                plt.imshow(img)
                print('点击所有倒立的汉字，按回车提交')
                points = plt.ginput(7)
                capt = json.dumps({'img_size': [200, 44],
                                   'input_points': [[i[0]/2, i[1]/2] for i in points]}) #除以2的原因是原图其实是400*88的，但是显示的时候变成了200*44
            else:
                img.show() 
                capt = input('请输入图片里的验证码：')
            # 这里必须先把参数 POST 验证码接口
            session.post(api, data={'input_text': capt}, headers=headers)
            return capt
        return ''

def get_token(login_url):
    '''
    读取网页内容，获得headers信息
    得到headers里面的的'Set-Cookie'内容
    并用正则匹配内部的_xsrf内容
    '''
    content=requests.get(login_url,headers=u_a)
    try:
        token = re.findall(r'_xsrf=([\w|-]+)', content.headers.get('Set-Cookie'))[0]
    except:
        pass
    print(token)
    return token

'''
建立时间戳
'''
timestamp=int(1000*time.time())

def get_signature(timestamp):
    '''
    在浏览器后台的调试器中找到signature所在的文件
    查看signature的获得方式
    发现是由grant_type+client_id+source外加时间戳加密获得的
    按照这种方式生成signature就好了
    '''
    ha=hmac.new(b'd1b964811afb40118a12068ff74a12f4',digestmod=hashlib.sha1)
    grant_type=login_data['grant_type']
    client_id=login_data['client_id']
    source=login_data['source']
    ha.update(bytes(grant_type+client_id+source+str(timestamp),'utf-8'))
    return ha.hexdigest()

def check_user_pass(login_data):
    '''
    默认以手机号的方式输入账户信息
    '''
    if login_data['username']=='':
        username=input('请输入用户名：')
        if '+86' not in username:
            username ='+86'+username
            login_data['username']=username
    if login_data['password']=='':
        password=input('请输入密码：')
        login_data['password']=password 
        
if __name__=='__main__':
    login(login_url)