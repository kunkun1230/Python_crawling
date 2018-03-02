# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 18:37:26 2018

@author: lenovo
"""

import os
from PIL import Image

path = "E:/数据学习资料/自己做的小项目/爬取简书推荐作者/src/"

dirlist = []

for root, dirs, files in os.walk(path):     
    for dir in dirs :
        dirlist.append(dir)
print(dirlist)

num = 0
for dir in dirlist:
    images = [] # images in each folder
    for root, dirs, files in os.walk(path+dir): # traverse each folder
        print(path+dir+'')
        i=1
        for file in files: #遍历文件夹中的每一个文件
            print(file)
            images.append(Image.open(path+dir+'/'+file))
            im=Image.open(path+dir+'/'+file)
            im=im.convert('RGBA')
            width, height = im.size
            width=100 #修改图片的宽度
            height=100 #修改图片的高度
            resizedim=im.resize((width,height)) #修改图片的尺寸
            name=path+str(i)+'.jpg' #定义图片名称
            resizedim.save(name) #保存图片
            i+=1