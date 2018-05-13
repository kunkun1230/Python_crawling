# -*- coding: utf-8 -*-
"""
Created on Mon May  7 09:20:17 2018

@author: lenovo
"""

import requests

#proxies={'http':'110.88.127.22:28100'}
#
url='http://www.baidu.com'

url1='http://api.ip.data5u.com/dynamic/get.html?order=7a8605c9cc612019e9d3bd7a3163723f&sep=3' #5u代理的ip链接测试

url2='http://space.bilibili.com'

data={'random':True,'ttl':'1'}

b=requests.get(url1,data=data).content

#b=requests.post(url1,data=data).content #post可以发送data数据，但是get是不行的

print(b)

#proxies={'http':str(b)[2:-3]}
#
#
#print(proxies)
#
#a=requests.get(url,proxies=proxies)
#
#print(a.status_code)
#
#print(a.content.decode("UTF-8"))

#url=''
#
#def getip(url):
#    ip=requests.get(url).content
#    return ip

#proxies = {
#    'http':'http://60.179.43.116:23343',
#    'http':'http://115.203.209.92:43200',
#    'http':'http://171.12.87.185:28947',
#    'http':'http://121.62.63.70:26872',
#    'http':'http://114.230.99.165:22223',
#    'http':'http://180.122.144.66:38047',
#    'http':'http://115.221.115.244:39604',
#    'http':'http://125.109.199.57:43462',
#    'http':'http://60.186.159.187:20152',
#    'http':'http://180.122.146.51:25191',
#    'http':'http://27.153.128.158:42633',
#    'http':'http://114.99.94.73:34715',
#    'http':'http://60.175.197.232:23844',
#    'http':'http://218.73.138.190:40784',
#    'http':'http://117.30.70.52:29312',
#    'http':'http://123.161.155.223:37309',
#    'http':'http://121.206.68.8:49325',
#    'http':'http://115.217.150.161:49781',
#    'http':'http://49.85.7.167:25189',
#    'http':'http://115.203.182.223:23526',
#    }
#
#proxies = {
#    'http': 'http://61.155.164.108:3128',
#    'http': 'http://116.199.115.79:80',
#    'http': 'http://42.245.252.35:80',
#    'http': 'http://106.14.51.145:8118',
#    'http': 'http://116.199.115.78:80',
#    'http': 'http://123.147.165.143:8080',
#    'http': 'http://58.62.86.216:9999',
#    'http': 'http://202.201.3.121:3128',
#    'http': 'http://119.29.201.134:808',
#    'http': 'http://61.155.164.112:3128',
#    'http': 'http://123.57.76.102:80',
#    'http': 'http://116.199.115.78:80',
#}