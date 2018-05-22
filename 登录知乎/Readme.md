# 知乎登陆程序更新

知乎的网页格式又更新了

针对最近的网页结构，进一步改进了一下知乎的登录代码

* 首先，用一个流程图说明整个登录的过程

![描述](https://github.com/kunkun1230/Python_crawling/blob/master/%E7%99%BB%E5%BD%95%E7%9F%A5%E4%B9%8E/Screenshots/1.png)

* 能够成功的登录知乎，向网页post所需的数据（headers和login_data）是关键
其中headers所必须的Key word如下：

其中的x-xsrftoken需要实时更新，以便可以获得最新的登陆验证码，否则会出现登陆验证码过期的提示

![描述](https://github.com/kunkun1230/Python_crawling/blob/master/%E7%99%BB%E5%BD%95%E7%9F%A5%E4%B9%8E/Screenshots/2.png)

login_data所必须的Key word如下:
![描述](https://github.com/kunkun1230/Python_crawling/blob/master/%E7%99%BB%E5%BD%95%E7%9F%A5%E4%B9%8E/Screenshots/3.png)

