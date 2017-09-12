# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup as bs

original_url='''https://movie.douban.com/top250'''

def getweb(html):
    return requests.get(html,headers={
            'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'
            }).content
    

def read_data(html):
    soup=bs(html,'lxml')
    Web=soup.find('ol',attrs={'class':'grid_view'})
    name=[]
    for each in Web.find_all('div',attrs={'class':'hd'}):
        a=each.find('span',attrs={'class':'title'}).getText()
        name.append(a)
    
    next_page=soup.find('span',attrs={'class':'next'}).find('a')
    while next_page:
        return name,original_url+next_page['href']
    return name,None
    
    
#    with open('Name','w',encoding='utf-8') as f:
#        for each in name:
#            f.write(each+'\n')
        
def main():
    url=original_url
    with open('Name','w',encoding='utf-8') as f:
        while url:
            html=getweb(url)
            name,url=read_data(html)
            for i in name:
                f.write(i+'\n')

if __name__=='__main__':
    main()
    
    
    
    
    
    