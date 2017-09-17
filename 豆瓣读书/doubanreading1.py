# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 21:59:01 2017

@author: lenovo
"""

import requests
from bs4 import BeautifulSoup as bs
import time

starttime=time.time()

def getweb(html): #读取网络信息
     return requests.get(html).content
 
def readweb(html):#读取网页上的数据
    soup=bs(html,'lxml')
    book=[]
    for li in soup.find_all('li',attrs={'class':'item store-item'}):
        tag_a=li.find('h4',attrs={'class':'title'})
        bookname=tag_a.find('a').getText()
        book.append(bookname)
    return book,soup

def main(): #将上面两个函数粘合起来
    url='https://read.douban.com/columns/category/all?sort=hot&start=0'
    page=1
 #------------------------开始写入网络数据工作----------------------------
    with open('Book','w',encoding='utf-8') as f: #打开文件确保数据可以一直写入文件而不被覆盖
        while url:
            html=getweb(url)
            book1,soup1=readweb(html)
            soup2=soup1.find('li',attrs={'class':'next'})
            if soup2.find('a'):
                url='https://read.douban.com'+str(soup2.find('a')['href'])
                page+=1
                print('已开始爬取%d页'%page) 
            else:
                url=None #确保在最后一页可以跳出while语句
            time.sleep(0.1)
            for i in book1:
                f.write(i+'\n')
#------------------------确定工作时间------------------------'''
    endtime=time.time()
    Duration=endtime-starttime
    print(Duration)

if __name__=='__main__':
    main()
        
    
        