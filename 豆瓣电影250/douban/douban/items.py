# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title= scrapy.Field()  #/html/body/div[3]/div[1]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a/span[1]/text()
    director= scrapy.Field()  #/html/body/div[3]/div[1]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[1]/text()
    rating_num= scrapy.Field()  #/html/body/div[3]/div[1]/div/div[1]/ol/li[1]/div/div[2]/div[2]/div/span[2]/text()
    comment_num= scrapy.Field()  #/html/body/div[3]/div[1]/div/div[1]/ol/li[1]/div/div[2]/div[2]/div/span[4]/text()
    quote= scrapy.Field()  #/html/body/div[3]/div[1]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[2]/span/text()  