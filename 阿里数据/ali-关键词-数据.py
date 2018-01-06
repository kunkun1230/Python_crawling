# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 19:25:06 2017

@author: lenovo
"""

import requests

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree #用xpath爬取数据
import time

browser = webdriver.Firefox()

url='https://job.alibaba.com/zhaopin/positionList.htm#page/1'

#headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#         'Accept-Encoding':'gzip, deflate, br',
#         'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#         'Cache-Control	':'max-age=0',
#         'Connection':'keep-alive',
#         'Cookie':'JSESSIONID=EF6Y9D1WO2-089Q3CJKMUFBB1VAC3WK3-E461JDBJ-LWGI5; tmp0=hr0tdxnMmMA54%2F1FFrwn%2BWwQouMRecZObHxzJ3CyXc4Jxl83x3rqNyRy4yF8d7QIIruEmZStGEERjqTHV4VmXvoi%2B0QSPde6iLx9GUtr%2BWparHVO%2FQ3FsTXbDW0AYTRmXkIg2NEyYG9knmB8JIrgprB1QlEsd46cB%2BvT7BOMnkYIpHj43N%2FYRDxNHrDFyx4r; UM_distinctid=1606e76977f41-09008ef8002763-4c322e7d-144000-1606e7697803db; CNZZDATA1000004769=163464961-1513680100-%7C1513682469',
#         'Host':'job.alibaba.com',
#         'Upgrade-Insecure-Requests':'1',
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}

def open_browser(url): #打开浏览器，并选择杭州，技术岗，输入关键词‘数据’进行查找
    browser.get(url)
    #选择杭州
    elem = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/div/div[1]/span/span/a[1]').click()
    time.sleep(2)
    #选择技术岗
    elem_1 = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/div/div[2]/span/a[3]').click()
    time.sleep(2)
    elem_2 = browser.find_element_by_id('keyword')
    #    elem_2.clear()
    #输入关键词“数据”
    elem_2.send_keys('数据'+Keys.RETURN)
    time.sleep(10)

def change_page():#定义翻页函数。试了好几种查找方式，发现xpath等效果都不好，只有这个link_text合适
    elem_3 = browser.find_element_by_link_text('>').click()
    
#------------------------读取招聘页面信息---------------------------------
def read_page():
    Content = browser.page_source
    return Content

def get_data(Content):
    selector=etree.HTML(Content)
    Job_information1=[]
    Job_information2=[]
    for i in range(1,20,2): #网页里面的很多信息的父节点相同，因此用Xpath爬取，并替换相应位置的数字会更快捷一些
        job_name=selector.xpath(r'/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[%s]/td[1]/span/a/text()'%(i))[0].strip()
        job_characteristic=selector.xpath(r'/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[%s]/td[2]/span/text()'%(i))[0].strip()
        job_location=selector.xpath(r'/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[%s]/td[3]/span/text()'%(i))[0].strip()
        recruit_number=selector.xpath(r'/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[%s]/td[4]/span/text()'%(i))[0].strip()
        job_updatetime=selector.xpath(r'/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[%s]/td[5]/span/text()'%(i))[0].strip()
        job_information1=job_name+'@'+job_characteristic+'@'+job_location+'@'+recruit_number+'@'+job_updatetime+'@' #用@替换便于后期在excel中分列
        Job_information1.append(job_information1)
    for j in range(2,21,2):
        job_description=selector.xpath(r'/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[%s]/td/div/p[1]/text()'%(j)) #岗位描述和岗位要求两个结果是列表
        job_request=selector.xpath(r'/html/body/div[4]/div[2]/div/div[2]/table/tbody/tr[%s]/td/div/p[2]/text()'%(j))
        job_Description=''
        job_Request=''
        for k in range(len(job_description)):
            job_Description+=job_description[k].strip()
        for h in range(len(job_request)):
            job_Request+=job_request[h].strip()
        job_information2=job_Description+'@'+job_Request
        Job_information2.append(job_information2)
    return Job_information1,Job_information2


if __name__=='__main__':
    with open(r'C:\Users\lenovo\Desktop\爬取阿里招聘数据\ali_data.txt','w',encoding='utf-8') as f1:
        open_browser(url)
        m=1
        print('浏览器已开启')
        while m <100:
            Content=read_page()
            print('第%s页已经读取'%m)
            Information1,Information2=get_data(Content)
            for l in range(10):
                Job_information=Information1[l]+Information2[l]+'\n'
                f1.write(Job_information)
            change_page()
            time.sleep(20)
            m+=1
            
    
    









