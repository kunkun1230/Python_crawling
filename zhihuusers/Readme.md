
## 使用Scrapy获取知乎关注者信息<br>
`逻辑：`<br>
<font color=#0099ff size=7 face="黑体">逻辑</font>
#### 1.以轮子哥的id为起点；<br>
爬取他的关注者及关注人信息
#### 2.获得这些人的url_token；<br>
由此构建对应的人物的关注者与关注人的url，并分别爬取
#### 3.将爬取到的数据去重并写入mongdb；<br>
如此递归下去，能够实现爬取所有人的关注者与关注人信息，只到所有人的信息都被爬取到为止
<br>
<br>
#### 主程序Spider的逻辑相对比较简单<br>
不过，要注意的是在其他几个文件中相应的设置：<br>
#### 1.Items文件
为了简单方便，可以直接
> from scrapy import Item,Field<br>
> class UsersItem(Item):<br>
> 　　　　id = Field()<br>
> 　　　　....<br>

这样就不用在程序的每个Item和Field前面都加上scrapy了

#### 2.pipeline文件
为了写入mongo，引入pymongo模块，其他的程序可以直接在scrapy官网复制
>import pymongo

最重要的一条写入命令为：
>self.db['user'].update({'url_token': item['url_token']}, dict(item), True)

主要的含义是：
>db.collection.update(<br>
>　　&lt;query&gt;,  # update的查询条件，类似sql update查询内where后面的<br>
>　　&lt;update&gt;, #  update的对象和一些更新的操作符（如$,$inc...）等，也可以理解为sql update查询内set后面的<br>
>　　{<br>
>　　　upsert: &lt;boolean&gt;, # 可选，这个参数的意思是，如果不存在update的记录，是否插入objNew,true为插入，默认是false，不插入。<br>
>　　　multi: &lt;boolean&gt;, # 可选，mongodb 默认是false,只更新找到的第一条记录，如果这个参数为true,就把按条件查出来多条记录全部更新<br>
>　　　writeConcern: &lt;document&gt; # 可选，抛出异常的级别。<br>
>　　}<br>
>)<br>

#### 3.setting文件
主要修改了请求头：
>DEFAULT_REQUEST_HEADERS<br>

机器人协议：
>ROBOTSTXT_OBEY = False<br>

pipeline接口:
>ITEM_PIPELINES = {<br>
>    'zhihuusers.pipelines.MongoPipeline': 300,<br>
>}<br>

mongo数据库的连接
>MONGO_URI= 'localhost'<br>
>MONGO_DATABASE='zhihu'<br>
