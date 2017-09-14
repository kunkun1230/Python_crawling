# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 22:49:56 2017

@author: lenovo
"""

import codecs
import requests
from bs4 import BeautifulSoup as bs

DOWNLOAD_URL = 'http://movie.douban.com/top250/'

def download_page(url):
    return requests.get(url,headers={
            'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'
            }).content

def parse_html(html):
    soup=bs(html,'html.parser')
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})

    movie_name_list = []

    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()

        movie_name_list.append(movie_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, None

def main():
    url=DOWNLOAD_URL
    
    with codecs.open('movies', 'w', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            for i in movies:
                fp.write(i+'\n') #这里fp一直是保持打开并写入状态，因此结果不会被冲掉
            # fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))

if __name__=='__main__':
    main()
    
    
