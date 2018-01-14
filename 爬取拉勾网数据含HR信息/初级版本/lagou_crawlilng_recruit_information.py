# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 19:57:30 2018

@author: lenovo
"""
import requests
from bs4 import BeautifulSoup as soup
import json
import time
import xlwt

url='https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE?labelWords=&fromSearch=true&suginput='
url1='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'

header={'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':'37',	
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',	
        'Cookie':'JSESSIONID=ABAAABAAAGFABEFC2C47AC9C9BDF567AC0BC0ECB7123BBF; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515670130; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515670171; _ga=GA1.2.509750146.1515670130; _gat=1; user_trace_token=20180111192849-980c5105-f6c2-11e7-898f-525400f775ce; LGSID=20180111192849-980c5295-f6c2-11e7-898f-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DLu_QNID5UG1wafe0G5iQeUErIpsMzZlTgqOLN9NjzmW%26wd%3D%26eqid%3D84739cd00002793c000000035a574a69; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20180111192930-b07dfa14-f6c2-11e7-898f-525400f775ce; LGUID=20180111192849-980c541e-f6c2-11e7-898f-525400f775ce; _gid=GA1.2.1599216201.1515670131; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; SEARCH_ID=03543a5de9464ac094d25c3cf461db19',	
        'Host':'www.lagou.com',	
        'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE?labelWords=&fromSearch=true&suginput=',	
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'X-Anit-Forge-Code':'0',	
        'X-Anit-Forge-Token':'None',	
        'X-Requested-With':'XMLHttpRequest',}

def form_data(i):
    data={'first':'True',
          'kd':'数据'}
    data['pn']=str(i)
    return data

#cookies={'cookies':'JSESSIONID=ABAAABAAAGFABEFC2C47AC9C9BDF567AC0BC0ECB7123BBF; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515670130; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515670171; _ga=GA1.2.509750146.1515670130; _gat=1; user_trace_token=20180111192849-980c5105-f6c2-11e7-898f-525400f775ce; LGSID=20180111192849-980c5295-f6c2-11e7-898f-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DLu_QNID5UG1wafe0G5iQeUErIpsMzZlTgqOLN9NjzmW%26wd%3D%26eqid%3D84739cd00002793c000000035a574a69; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20180111192930-b07dfa14-f6c2-11e7-898f-525400f775ce; LGUID=20180111192849-980c541e-f6c2-11e7-898f-525400f775ce; _gid=GA1.2.1599216201.1515670131; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; SEARCH_ID=03543a5de9464ac094d25c3cf461db19'}

def get_link(data):
    link=requests.post(url=url1,data=data,headers=header,timeout=20).content
    return link

def get_information(link):
    result=json.loads(link,strict=False)
    position_results=result['content']['positionResult']['result']
    Job_list=[]
    for job in position_results:
        Job_detail=[]
        companyId=Job_detail.append(job['companyId'])
        positionId=Job_detail.append(job['positionId'])
        positionName=Job_detail.append(job['positionName'])
        createTime=Job_detail.append(job['createTime'])
        positionAdvantage=Job_detail.append(job['positionAdvantage'])
        workYear=Job_detail.append(job['workYear'])
        education=Job_detail.append(job['education'])
        city=Job_detail.append(job['city'])
        industryField=Job_detail.append(job['industryField'])
        financeStage=Job_detail.append(job['financeStage'])
        companyLabelList=Job_detail.append(job['companyLabelList'])
        companySize=Job_detail.append(job['companySize'])
        positionLables=Job_detail.append(job['positionLables'])
        longitude=Job_detail.append(job['longitude'])
        latitude=Job_detail.append(job['latitude'])
        firstType=Job_detail.append(job['firstType'])
        secondType=Job_detail.append(job['secondType'])
        companyFullName=Job_detail.append(job['companyFullName'])
        Job_list.append(Job_detail)
    return Job_list
#        companyId=job['companyId']
#        positionId=job['positionId']
#        positionName=job['positionName']
#        createTime=job['createTime']
#        positionAdvantage=job['positionAdvantage']
#        workYear=job['workYear']
#        education=job['education']
#        city=job['city']
#        industryField=job['industryField']
#        financeStage=job['financeStage']
#        companyLabelList=job['companyLabelList']
#        companySize=job['companySize']
#        positionLables=job['positionLables']
#        longitude=job['longitude']
#        latitude=job['latitude']
#        firstType=job['firstType']
#        secondType=job['secondType']
#        companyFullName=job['companyFullName']
        

if __name__ == '__main__':
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    row0=['companyId','positionId','positionName','createTime','positionAdvantage','workYear',
          'education','city','industryField','financeStage','companyLabelList','companySize',
          'positionLables','longitude','latitude','firstType','secondType','companyFullName']
    for item in range(len(row0)):
        sheet1.write(0,item,row0[item])
    Jobs=[]
    for i in range(0,30):
        print('读取第%s页面数据'%i)
        Data=form_data(i+1)
        Link=get_link(Data)
        Jobs+=get_information(Link)
    print(Jobs)
    print('开始写入excel')
    for j in range(len(Jobs)):
        print('写入第%s行数据'%j)
        for k in range(len(Jobs[0])):
            sheet1.write(j+1,k,str(Jobs[j][k]))
    
    f.save(r'E:\数据学习资料\自己做的小项目\爬取拉勾网数据\Jobs.xls')
    
    
    





