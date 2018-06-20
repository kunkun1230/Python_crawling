# -*- coding: utf-8 -*-
"""
Created on Sun May 13 16:58:44 2018

@author: lenovo
"""


import requests
from lxml import etree

#start_urls = 'https://www.baidu.com/'
#
#url='http://www.xicidaili.com/'
#
#headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
#
#text=requests.get(url,headers=headers).content
#
#text=str(text,encoding='utf-8')
#
##with open('xici.txt','w',encoding='utf-8') as f:
##    f.write(text)
#selector=etree.HTML(text)
#
#a=selector.xpath(r'/html/body/div[1]/div[1]/h1/text()')
##a=selector.xpath(r'/html/body/div[@id="wrapper"]/div[@id="body"]/div[1]/div[1]/table/tr[@class="subtitle"]/th[2]/text()')
#
#print(a)


#----------------------测试豆瓣----------------------------------------------------------------------------

#headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
#
#start_url='https://movie.douban.com/top250'
#
#text=requests.get(start_url,headers=headers).content
#
##text=str(text,encoding='utf-8')
#
#selector=etree.HTML(text)
#
#a=selector.xpath(r'/html/body/div[3]/div[1]/div/div[1]/ol/li')
#
#for each in a:
#    title=each.xpath(".//div[@class='hd']/a/span[1]/text()")[0]
#    print(title)
#    director=each.xpath(".//div[@class='bd']/p/text()")[0].strip()
#    print(director)
#    rating_num=each.xpath(".//div[@class='star']/span[4]/text()")[0]
#    print(rating_num)
#    comment_num=each.xpath(".//div[@class='star']/span[2]/text()")[0]
#    print(comment_num+'分')
#    quote=each.xpath(".//div[@class='bd']/p[@class='quote']/span/text()")[0]
#    print(quote+'\n')

#def prase(self,response):
#    item=DoubanItem()
#    content=response.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li')
#    for each in content:
#        item['title']=each.xpath(".//div[@class='hd']/a/span[1]/text()").extract()[0]
#        item['director']=each.xpath(".//div[@class='bd']/p/text()").extract()[0]
#        item['rating_num']=each.xpath(".//div[@class='start']/span[4]/text()").extract()[0]
#        item['comment_num']=each.xpath(".//div[@class='hd']/a/span[1]/text()").extract()[0]
#        item['quote']=each.xpath(".//div[@class='bd']/p/span/text()").extract()[0]
#        yield item

from PIL import Image
import matplotlib.pyplot as plt

#读取图像转换为灰度图像并保存到数组
im = Image.open(r"C:\Users\lenovo\Desktop\123.jpg")

plt.imshow(im)
print('Please click 3 points')
x = plt.ginput(3)

print('you clicked:',x)