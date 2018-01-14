# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 20:41:00 2018

@author: lenovo
"""

import requests
from bs4 import BeautifulSoup as soup
import json
import time
import xlrd
from lxml import etree
import random

header={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'JSESSIONID=ABAAABAAAGFABEFC2C47AC9C9BDF567AC0BC0ECB7123BBF; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515670130; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515850149; _ga=GA1.2.509750146.1515670130; user_trace_token=20180111192849-980c5105-f6c2-11e7-898f-525400f775ce; LGRID=20180113212907-bb71206f-f865-11e7-9459-525400f775ce; LGUID=20180111192849-980c541e-f6c2-11e7-898f-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; SEARCH_ID=ac4cde1786eb478597fda9e9df960a1b; _gid=GA1.2.970970505.1515822147; X_HTTP_TOKEN=2a314f0c0c7010eee4d3e02e74b6de98; _gat=1; LGSID=20180113212755-908096a3-f865-11e7-a2e7-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2595%25B0%25E6%258D%25AE%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3880723.html',	
        'Host':'www.lagou.com',	
        'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE?labelWords=&fromSearch=true&suginput=',	
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        }

data=xlrd.open_workbook(r'E:\数据学习资料\自己做的小项目\爬取拉勾网数据\Jobs.xls')
table=data.sheets()[0]
link_list=table.col_values(18)

    
def get_url(url):
     Content=requests.get(url,headers=header,timeout=100).content
     return Content

def get_information(Content):
    selector=etree.HTML(Content)
    try:
        #-----------------聊天意愿--------------------------
        Willing=selector.xpath(r'/html/body/div[4]/div[1]/dl[1]/dd[4]/div/div[2]/div[1]/span[3]/text()') #聊天意愿快慢
        feedback=selector.xpath(r'/html/body/div[4]/div[1]/dl[1]/dd[4]/div/div[2]/div[1]/span[4]/i[1]/text()') #回复率
        Time_1=selector.xpath(r'/html/body/div[4]/div[1]/dl[1]/dd[4]/div/div[2]/div[1]/span[4]/i[2]/text()') #回复率用时
        #----------------七日内简历处理效率-----------------
        Response=selector.xpath(r'/html/body/div[4]/div[1]/dl[1]/dd[4]/div/div[2]/div[2]/span[3]/text()') #7日内职位发布者简历处理的效率
        Percent=selector.xpath(r'/html/body/div[4]/div[1]/dl[1]/dd[4]/div/div[2]/div[2]/span[4]/i[1]/text()') #处理率
        Time_2=selector.xpath(r'/html/body/div[4]/div[1]/dl[1]/dd[4]/div/div[2]/div[2]/span[4]/i[2]/text()') # 处理用时
        #----------------活跃时段---------------------------
        Active=selector.xpath(r'/html/body/div[4]/div[1]/dl[1]/dd[4]/div/div[2]/div[3]/span[3]/text()')     #1个月内职位发布者整体活跃情况统计
        Time_zone=selector.xpath(r'/html/body/div[4]/div[1]/dl[1]/dd[4]/div/div[2]/div[3]/span[4]/text()')  # 哪个时间段最活跃                                                                                             #1个月内职位发布者最活跃时段
        Clock=selector.xpath(r'/html/body/div[4]/div[1]/dl[1]/dd[4]/div/div[2]/div[3]/span[4]/i/text()')    #最活跃的时间
        
        print(Willing,feedback,Time_1,Response,Percent,Time_2,Active,Clock)
        condition=Willing[0]+'@'+feedback[0]+'@'+Time_1[0]+'@'+Response[0]+'@'+Percent[0]+'@'+Time_2[0]+'@'+Active[0]+'@'+Time_zone[0]+'@'+Clock[0]+'\n'
    except IndexError:
        condition=' '
    return condition

if __name__=='__main__':
    with open(r'E:\数据学习资料\自己做的小项目\爬取拉勾网数据\response.txt','w',encoding='utf-8') as f:
        for i in range(len(link_list)):
            url=link_list[i+1]
            print(url)
            Content=get_url(url)
            time.sleep(random.choice(range(1,3)))
            Condition=get_information(Content)
            f.write(Condition)
    
