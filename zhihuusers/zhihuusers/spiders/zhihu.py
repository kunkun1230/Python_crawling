# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import json
from zhihuusers.items import UsersItem

class ZhihuSpider(Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']
    
    start_user = 'excited-vczh'
    
    user_url='https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query='allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
        
    follows_url='https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followers_url='https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'


    def start_requests(self):
#        url='https://www.zhihu.com/api/v4/members/ya-ya-yi-17?include=allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
        
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query),self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),self.parse_follows)
        yield Request(self.followers_url.format(user=self.start_user,include=self.followers_query,offset=0,limit=20),self.parse_followers)
  
        
    def parse_user(self, response):
        result=json.loads(response.text)
        
        item = UsersItem()
        for field in item.fields:
            if field in result.keys():
                item[field]=result.get(field)
        yield item
        yield Request(self.follows_url.format(user=item['url_token'],include=self.follows_query,offset=0,limit=20),self.parse_follows)
        yield Request(self.followers_url.format(user=item['url_token'],include=self.followers_query,offset=0,limit=20),self.parse_followers)

    
    def parse_followers(self, response):
        result=json.loads(response.text)
        
        if 'data' in result.keys():
            for each in result['data']:   
                yield Request(self.user_url.format(user=each.get('url_token'),include=self.user_query),self.parse_user)
        
        if 'paging' in result.keys() and result['paging']['is_end']== False:   #这里的false是布尔符号，不是字符串
                next_url=result['paging']['next']
                yield Request(next_url,self.parse_followers)

    
    def parse_follows(self, response):
        result=json.loads(response.text)
        
        if 'data' in result.keys():
            for each in result['data']:   
                yield Request(self.user_url.format(user=each.get('url_token'),include=self.user_query),self.parse_user)
        
        if 'paging' in result.keys() and result['paging']['is_end']== False:   #这里的false是布尔符号，不是字符串
                next_url=result['paging']['next']
                yield Request(next_url,self.parse_follows)

        