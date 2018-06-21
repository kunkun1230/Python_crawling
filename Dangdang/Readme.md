## 使用Scrapy获取当当特产目下的产品信息<br>
### 1.创建Scrapy文件；<br> 
指定目录下输入`scrapy startproject Dangdang`<br> 
### 2.items文件创建并修改；<br>
确定需要爬取的信息
### 3.pipeline文件修改；<br>
选择输出的文件类型，并编写保存文件格式
### 4.setting文件修改；<br>
`ROBOTSTXT_OBEY = True`<br>
`COOKIES_ENABLED = False`<br>
`ITEM_PIPELINES = {
    'Dangdang.pipelines.DangdangPipeline': 300,
}`
### 5.编写爬虫主文件<br>
`scrapy genspider autospd dangdang.com`
