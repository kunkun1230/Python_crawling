# -*- coding: utf-8 -*-
import scrapy
from Dangdang.items import DangdangItem
from scrapy.http import Request

class AutopsdSpider(scrapy.Spider):
    name = "autopsd"
    allowed_domains = ["dangdang.com"]
    start_urls = ['http://category.dangdang.com/pg1-cid4011029.html']  

    def parse(self, response):
        item=DangdangItem()
        item['name']=response.xpath("//a[@dd_name='单品标题']/text()").extract()
        item['price']=response.xpath("//span[@class='price_n']/text()").extract()
        item['link']=response.xpath("//a[@class='pic']/@href").extract()
        item['comnum']=response.xpath("//a[@dd_name='单品评论']/text()").extract()
        yield item
        for i in range(1,100):
            url="http://category.dangdang.com/pg"+str(i)+"-cid4011029.html"
            yield Request(url,callback=self.parse)