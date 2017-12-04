# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 23:43:01 2017

@author: lenovo
"""

#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @Time   : 2017/3/28 8:46
# @Author : Lyrichu
# @Email  : 919987476@qq.com
# @File   : NetCloud_spider3.py
'''
@Description:
网易云音乐评论爬虫，可以完整爬取整个评论
部分参考了@平胸小仙女的文章(地址:https://www.zhihu.com/question/36081767)
post加密部分也给出了，可以参考原帖：
作者：平胸小仙女
链接：https://www.zhihu.com/question/36081767/answer/140287795
来源：知乎
'''
from Crypto.Cipher import AES
import base64
import requests
import json
import codecs
import time
import random

# 头部信息 #需根据自己浏览器的信息进行替换
headers={'Host':'music.163.com',
         'Accept':'*/*',
         'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
         'Accept-Encoding':'gzip, deflate',
         'Content-Type':'application/x-www-form-urlencoded',
         'Referer':'http://music.163.com/song?id=347597',
         'Content-Length':'484',
         'Cookie':'__s_=1; _ntes_nnid=f17890f7160fd145486752ebbf2066df,1505221478108; _ntes_nuid=f17890f7160fd145486752ebbf2066df; JSESSIONID-WYYY=Z99pE%2BatJVOAGco1d%2FJpojOK94Xe9GHqe0epcCOj23nqP2SlHt1XwzWQ2FXTwaM2xgIN628qJGj8%2BikzfYkv%2FXAUo%2FSzwMxjdyO9oeQlGKBvH6nYoFpJpVlA%2F8eP57fkZAVEsuB9wqkVgdQc2cjIStE1vyfE6SxKAlA8r0sAgOnEun%2BV%3A1512200032388; _iuqxldmzr_=32; __utma=94650624.1642739310.1512184312.1512184312.1512184312.1; __utmc=94650624; __utmz=94650624.1512184312.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); playerid=10841206',	
         'Connection':'keep-alive',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}

# offset的取值为:(评论页数-1)*20,total第一页为true，其余页为false
# first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}' # 第一个参数
second_param = "010001" # 第二个参数
# 第三个参数
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# 第四个参数
forth_param = "0CoJUm6Qyw8W8jud"

# 获取参数
def get_params(page): # page为传入页数
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1): # 如果为第一页
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page-1)*20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset,'false')
        h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

# 获取 encSecKey
def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


# 解密过程
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = str(encrypt_text, encoding="utf-8") #注意一定要加上这一句，没有这一句则出现错误
    return encrypt_text

# 获得评论json数据
def get_json(url, params, encSecKey):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content

# 抓取热门评论，返回热评列表
def get_hot_comments(url):
    hot_comments_list = []
    hot_comments_list.append(u"用户ID 用户昵称 用户头像地址 评论时间 点赞总数 评论内容\n")
    params = get_params(1) # 第一页
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text)
    hot_comments = json_dict['hotComments'] # 热门评论
    print("共有%d条热门评论!" % len(hot_comments))
    for item in hot_comments:
            comment = item['content'] # 评论内容
            likedCount = item['likedCount'] # 点赞总数
            comment_time = item['time'] # 评论时间(时间戳)
            userID = item['user']['userID'] # 评论者id
            nickname = item['user']['nickname'] # 昵称
            avatarUrl = item['user']['avatarUrl'] # 头像地址
            comment_info = str(userID) + " " + str(nickname) + " " + str(avatarUrl) + " " + str(comment_time) + " " + str(likedCount) + " " + str(comment) + "\n"
            hot_comments_list.append(comment_info)
    return hot_comments_list

# 抓取某一首歌的全部评论
def get_all_comments(url):
    all_comments_list = [] # 存放所有评论
    all_comments_list.append(u"用户ID 用户昵称 用户头像地址 评论时间 点赞总数 评论内容\n") # 头部信息
    params = get_params(1)
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text)
    comments_num = int(json_dict['total'])
    if(comments_num % 20 == 0):
        page = comments_num / 20
    else:
        page = int(comments_num / 20) + 1
    print("共有%d页评论!" % page)
    for i in range(page):  # 逐页抓取
        params = get_params(i+1)
        encSecKey = get_encSecKey()
        json_text = get_json(url,params,encSecKey)
        json_dict = json.loads(json_text)
        if i == 0:
            print("共有%d条评论!" % comments_num) # 全部评论总数
        for item in json_dict['comments']:
            comment = item['content'] # 评论内容
            likedCount = item['likedCount'] # 点赞总数
            comment_time = item['time'] # 评论时间(时间戳)
            userID = item['user']['userId'] # 评论者id
            nickname = item['user']['nickname'] # 昵称
            avatarUrl = item['user']['avatarUrl'] # 头像地址
            comment_info = str(userID) + " " + str(nickname) + " " + str(avatarUrl) + " " + str(comment_time) + " " + str(likedCount) + " " + str(comment) + "\n"
            all_comments_list.append(comment_info)
        print("第%d页抓取完毕!" % (i+1))
        #time.sleep(random.choice(range(1,3))) 
    return all_comments_list

# 将评论写入文本文件
def save_to_file(list,filename):
        with open(filename,'a',encoding='utf-8') as f:
            f.writelines(list)
        print("写入文件成功!")

if __name__ == "__main__":
    start_time = time.time() # 开始时间
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_347597?csrf_token=" #替换为你想下载的歌曲R_SO的链接
    filename = "不再犹豫.txt" #修改歌曲名称
    all_comments_list = get_all_comments(url)
    save_to_file(all_comments_list,filename)
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))