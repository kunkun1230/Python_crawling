# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 22:05:57 2017

@author: lenovo
"""

import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import re
import json
import time 
import random

headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'_zap=3b7dc78d-5ef5-424d-9619-e3c7fcffeb61; d_c0="AGACjfTWCQyPTuyFGC_I5X5LoymJMXqZdgo=|1499598759"; q_c1=967348c7b1414a3b9bd9d3898aded2be|1503926087000|1499598273000; q_c1=d952fbc654044b5088074e95203f1fb1|1506646018000|1499598273000; _xsrf=d988f6dd72f2c9a6b54ce97912142400; aliyungf_tc=AQAAAHTQuzN38gsAGqnOtzXZLy8y99In; r_cap_id="ZjAxYzIwNDljZTBkNDE5Njg2ZjhmNDMyOTYwZjQwMmQ=|1508939677|bb73a1f0ab056ef6ff7f13ddc24d9c3cb7e9b8d4"; cap_id="YWFjNDI4NTY3ZWFmNDUxYmFmNWM2Mzc3MTA1MGIwN2E=|1508939677|577b012fa03fb6b23d027447ce9e0d4bc350e1f7"; __utma=51854390.1550210267.1506646046.1508858629.1508939555.13; __utmc=51854390; __utmz=51854390.1508855862.11.5.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/kunkun_1230/followers; __utmv=51854390.100-1|2=registration_date=20151218=1^3=entry_date=20151218=1; capsion_ticket="2|1:0|10:1508940264|14:capsion_ticket|44:MWE3MGRhNDUyNzgwNDFkNjg0NDJlNzNlZGQzMGRhYzI=|09e0328eafb81e589fd1dc5dcdfbad23ef231330649ca34d037d66a24356472b"; _xsrf=d988f6dd72f2c9a6b54ce97912142400',
'Host':'www.zhihu.com',
'Referer':'https://www.zhihu.com/topic/19559424/followers',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}



def read_link(url): #读取关注者的个人主页
    return requests.get(url,headers=headers).content

    
def get_data(link): #爬取关注者的个人信息
    soup=bs(link,'html.parser')
#    with open(r'.\followerpage.txt','w',encoding='utf-8') as f:
#        soup1=soup.prettify()
#        f.write(str(soup1))
    data=re.findall(r"data-state='(.*?)'",str(soup)) #用正则的方式找到关注者信息存放的位置data-state
    return data

def get_data_list(data):
    data_list=json.loads(data[0],strict=False) #将数据json化，便于提取
    follower_data=data_list['entities']['users'][follower_name_eng]
    #print(follower_data)
    #follower_data_detail=[]
    follower_name=follower_data['name'] #可以按照不同的key值来查找相关的信息了
    #follower_data_detail.append(follower_name)
    #----------------为了避免有些关注者的信息填写不完整，这里加入try...except语句试错
    try:
        follower_gender=follower_data['gender']
    except:
        follower_gender='性别未知'
    #print(follower_gender)
    #follower_data_detail.append(follower_gender)
    
    try:
        follower_location=follower_data['locations'][0]['name']
    except:
        follower_location='地址未知'
    #print(follower_location)
    #follower_data_detail.append(follower_location)
    
    try:
        follower_employments=follower_data['employments'][0]['company']['name'] #有些人可能写自己所在的很多公司，这里只考虑第一个
    except:
        follower_employments='工作未知'
    #print(follower_employments)
    #follower_data_detail.append(follower_employments)
    
    try:
         follower_educations_1=follower_data['educations'][0]['school']['name'] #同工作
         follower_educations_2=follower_data['educations'][0]['major']['name']
         follower_educations=follower_educations_1+','+follower_educations_2
    except:
         follower_educations='教育情况未知'
    #print(follower_educations)
    #follower_data_detail.append(follower_educations)
     
    try:
        follower_answerCount=follower_data['answerCount']
    except:
        follower_answerCount='回答问题数未知'
    #print(follower_answerCount)
    #follower_data_detail.append(follower_answerCount)
    
    try:
        follower_voteupCount=follower_data['voteupCount']
    except:
        follower_voteupCount='被赞次数未知'
    #print(follower_voteupCount)
    #follower_data_detail.append(follower_voteupCount)
    
    try:
        follower_followingCount=follower_data['followingCount']
    except:    
        follower_followingCount='关注人数未知'
    #print(follower_followingCount)
    #follower_data_detail.append(follower_followingCount)
    
    try:
        follower_followerCount=follower_data['followerCount']
    except:
        follower_followerCount='关注粉丝数未知'
    #print(follower_followerCount)
    #follower_data_detail.append(follower_followerCount) 
    
    try:
        follower_articlesCount=follower_data['articlesCount']
    except:
        follower_articlesCount='文章数量未知'
    #print(follower_articlesCount)
    #follower_data_detail.append(follower_articlesCount)  
    
    try:
        follower_questionCount=follower_data['questionCount']
    except:
        follower_questionCount='发布问题数未知'
    #print(follower_questionCount)
    #follower_data_detail.append(follower_questionCount)  
    
    detail=str(follower_name)+','+str(follower_gender)+','+str(follower_location)+','+str(follower_employments)+\
    ','+str(follower_educations)+','+str(follower_answerCount)+','+str(follower_voteupCount)+','+str(follower_followingCount)\
    +','+str(follower_followerCount)+','+str(follower_articlesCount)+','+str(follower_questionCount)+'\n'
    print(detail)
    return detail #刚开始没有将每一项字符化，发现IDLE虽然没有提示错误，但是没有结果产生
#    print(follower_data_detail)
#    return follower_data_detail
    
with open(r'C:\Users\lenovo\Desktop\关注数据分析话题的人\follower_link.txt','r',encoding='utf-8') as f:
    with open(r'C:\Users\lenovo\Desktop\关注数据分析话题的人\follower_data.txt','w',encoding='utf-8') as f1:
        for i in range(0,9980): #中间发现采集数据太频繁,大约在每1700条数据的时候就没有新的数据更新了，应该是被网站发现了
           try: 
                url=f.readline()
                follower_name_eng=re.findall(r'people/(.*?)\n',url)[0] #每一个链接后面都有一个换行符，一定要注意，后面使用json的键值会有问题
                link=read_link(url)
                data=get_data(link)
                f1.write(get_data_list(data))
                print('第%s位关注者数据已采集完毕'%(i+1))
                time.sleep(random.choice(range(1,3))) #中间有几次爬的时候被知乎发现而中断了，因此这里设置随机的时间间隔
           except:
                pass        
        