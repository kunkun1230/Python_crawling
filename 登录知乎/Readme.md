# 知乎登陆程序更新

知乎的网页格式又更新了

针对最近的网页结构，进一步改进了一下知乎的登录代码

* 首先，用一个流程图说明整个登录的过程

![描述](https://github.com/kunkun1230/Python_crawling/blob/master/%E7%99%BB%E5%BD%95%E7%9F%A5%E4%B9%8E/Screenshots/1.png)

* 能够成功的登录知乎，向网页post所需的数据（headers和login_data）是关键

  * 其中`headers`所必须的Key word如下：    
![描述](https://github.com/kunkun1230/Python_crawling/blob/master/%E7%99%BB%E5%BD%95%E7%9F%A5%E4%B9%8E/Screenshots/3.png)
  * `authorization`是不变的。headers里面唯一需要实时获得的就是`x-xsrftoken`，可以通过读取登陆页的headers，并解析其中的set—cookie获得<br>
  * `login_data`所必须的Key word如下:
![描述](https://github.com/kunkun1230/Python_crawling/blob/master/%E7%99%BB%E5%BD%95%E7%9F%A5%E4%B9%8E/Screenshots/2.png)<br>
  * `signature`通过ctrl+shift+F在网页的调试器中获得。打开js文件可以看到是通过hmac加密的，只要生成一个这样的文件即可
![描述](https://github.com/kunkun1230/Python_crawling/blob/master/%E7%99%BB%E5%BD%95%E7%9F%A5%E4%B9%8E/Screenshots/5.png)<br>
![描述](https://github.com/kunkun1230/Python_crawling/blob/master/%E7%99%BB%E5%BD%95%E7%9F%A5%E4%B9%8E/Screenshots/4.png)<br>
  * `captcha`是由更新xsrf后的headers通过get api后获得的。另写一个输入验证码的函数

* 明确了大方向后，逐一写出函数得到每个参数值，然后封装进login函数就可以实现登陆了

* 技能点：<br>
  * 加密：通过hmac和hashlib加密，获得signature；<br>
  * 破解图片验证码（PIL包）与文字验证码（matplotlib获得文字坐标）；<br>
  * session的作用，获得cookies
