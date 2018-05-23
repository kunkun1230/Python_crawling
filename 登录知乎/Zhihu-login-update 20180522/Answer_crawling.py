# -*- coding: utf-8 -*-
"""
Created on Mon May 21 10:33:48 2018

@author: kunkun_1230
"""
import requests
import zhihu_login as zh
import chardet
import json

'''
url='https://www.zhihu.com/people/kunkun_1230/followers'
follower_url='	http://www.zhihu.com/api/v4/members/kunkun_1230/followers?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'
'''

login_url='https://www.zhihu.com/signup'
xiaomi_url='https://www.zhihu.com/api/v4/questions/277333550/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=5&sort_by=default&offset='

#HEADERS={
#         'Connection':'keep-alive',
#         'Host':'www.zhihu.com',
#         'Referer':'https://www.zhihu.com',
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
#         }

zh.login(login_url) #确定知乎可以登录，并用session存储cookies和headers

resp=zh.session.get(xiaomi_url+'0') #读取想要爬取的知乎回答问题网页内容

print(chardet.detect(resp.content)) #查看此网页的编程语言及时转化，避免出现转码错误

Content=json.loads(resp.content) #载入读取的网页内容，json化

total_num=Content['paging']['totals']

for i in range(int(total_num/5)+1):
    new_url = xiaomi_url+str(5*i)
    res=zh.session.get(new_url)
    text=json.loads(res.content)
    try:
        for j in range(5):        
            print(text['data'][j]['content'])
    except IndexError:
        print('已爬取所有答案')