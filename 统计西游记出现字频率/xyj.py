# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 10:36:02 2017

@author: lenovo
"""

fr=open('xyj.txt','r',encoding='utf-8')

character = []
stat = {}

for line in fr:
    line=line.strip()

    if len(line)==0:
        continue

    line=str(line)

    for x in range(0,len(line)):
        if not line[x] in character:
            character.append(line[x])

        if line[x] not in stat:
            stat[line[x]]=0
        stat[line[x]]+=1

#print(len(character))
#print(len(stat))



stat = sorted(stat.items(),key=lambda d:d[1],reverse=True)
print(type(stat))

f2=open('stat.txt','w',encoding='utf-8')
for each in stat:
    f2.write(str(each[0])+','+str(each[1])+'\n')

f2.close()