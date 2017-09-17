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
    Subnumber=[]
    for li in soup.find_all('li',attrs={'class':'item store-item'}):
        tag_a=li.find('h4',attrs={'class':'title'})
        bookname=tag_a.find('a').getText()
        book.append(bookname)
        subhtml=tag_a.find('a')['href'] #获得每本书的独立链接
        sp=bs(getweb(subhtml),'lxml') #取得独立链接后读取
        try: #爬取的过程中发现，有些作品的评论太少，而导致没有评分，因此引入try
            number=sp.find('span',attrs={'class':'score'}).string
        except AttributeError:
            number=' '
        Subnumber.append(number)
    print(book)
    print(Subnumber)
    return book,soup,Subnumber


def main(): #将上面两个函数粘合起来

 #------------------------开始写入网络数据工作----------------------------
    with open('Book+Score','w',encoding='utf-8') as f: #打开文件确保数据可以一直写入文件而不被覆盖
        for i in range(0,2560,10):
                 url='https://read.douban.com/columns/category/all?sort=hot&start='+str(i)
                 html=getweb(url)
                 book1,soup1,Subnumber1=readweb(html)         
                 time.sleep(0.1)
                 for j in range(10):
                    f.write(book1[j]+' 评分'+Subnumber1[j]+'\n')
                 print('已读取第%d页'%(i/10)) #建议加入print，以反映当前爬取进度
                 time.sleep(0.1)
#------------------------确定工作时间------------------------'''
    endtime=time.time()
    Duration=endtime-starttime
    print(Duration)

if __name__=='__main__':
    main()
        
    
        