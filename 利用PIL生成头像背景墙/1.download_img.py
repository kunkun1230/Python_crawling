# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 23:00:12 2018

@author: lenovo
"""

import urllib.request
import time
import random

with open('.\src.txt','r',encoding='utf-8') as f:
    i=1
    for each in f:
        urllib.request.urlretrieve(('https:'+each),(str(i)+ ".jpg"))
        i+=1
        print(i)
        time.sleep(random.choice(range(1,3)))
        