# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 20:47:56 2017

@author: lenovo
"""

import requests
from lxml import etree

url='http://www.xicidaili.com/nn/'

headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}

#for i in range(10):
#    url=url+str(i+1)

def read_data(url):
    proxies=[]
    for i in range(10):
        url=url+str(i+1)
        link=requests.get(url,headers=headers).content #这一步提取出来的文件还是bytes形式的内容
        print(type(link))
        link=str(link,encoding='utf-8')
        print(type(link))
        #print(link)
        html=etree.HTML(link)
        ips=html.xpath('//html/body/div[1]/div[2]/table[@id="ip_list"]/tr[@class]/td[2]/text()')
        ports=html.xpath('//html/body/div[1]/div[2]/table[@id="ip_list"]/tr[@class]/td[3]/text()')
        for j in range(len(ips)):
            proxy='http:\\'+ips[j]+':'+ports[j]
            proxies.append(proxy)
        print('第%s页IP已经爬取'%(i+1))
        print(len(proxies))
    return proxies

def write_data(proxies):
    with open('proxies.txt','w',encoding='utf-8')as f:
        for each in proxies:
            f.write(each+'\n')
            
if __name__=='__main__':
    proxies=read_data(url)
    write_data(proxies)
    