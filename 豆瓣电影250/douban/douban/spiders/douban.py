# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:07:47 2018

@author: lenovo
"""

import scrapy
from scrapy import Request
from douban.items import DoubanItem

class DoubanSpider(scrapy.spiders.Spider):
    name = 'douban'
    start_urls = ['https://movie.douban.com/top250']
    headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    
    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        item = DoubanItem()
        movies = response.xpath(r'/html/body/div[3]/div[1]/div/div[1]/ol/li')
        for each in movies:
            item['title']=each.xpath(".//div[@class='hd']/a/span[1]/text()").extract()[0]
            item['director']=each.xpath(".//div[@class='bd']/p/text()").extract()[0].strip()
            item['rating_num']=each.xpath(".//div[@class='star']/span[4]/text()").extract()[0]
            item['comment_num']=each.xpath(".//div[@class='star']/span[2]/text()").extract()[0]
            try:
                item['quote']=each.xpath(".//div[@class='bd']/p[@class='quote']/span/text()").extract()[0]
            except:
                item['quote']=''
        
#        item['title']=response.xpath("/html/body/div[3]/div[1]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a/span[1]/text()").extract()[0]
#        item['director']=response.xpath("/html/body/div[3]/div[1]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[1]/text()").extract()[0].strip()
#        item['rating_num']=response.xpath("/html/body/div[3]/div[1]/div/div[1]/ol/li[1]/div/div[2]/div[2]/div/span[2]/text()").extract()[0]
#        item['comment_num']=response.xpath("/html/body/div[3]/div[1]/div/div[1]/ol/li[1]/div/div[2]/div[2]/div/span[4]/text()").extract()[0]
#        item['quote']=response.xpath("/html/body/div[3]/div[1]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[2]/span/text()").extract()[0]
            
            yield item
        
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url, headers=self.headers)

        
        