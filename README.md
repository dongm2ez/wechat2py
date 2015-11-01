#Wechat2py
  python接入微信开发者平台项目
##项目环境

    Ubuntu 14.04<br/>Apache 2.4.7<br/>Django 1.8.5<br/>
    
###项目思路

    1.首先因为要实现功能就是微信公众平台的网页授权获得用户信息，因此需要有一个接入微信公众平台的方法。
    2.微信是目前应用最广泛的社交app，而python以简单、优雅为编程哲学，因此喜欢发明轮子的python社区很大可能会有相应的开发sdk，可以安装应用， 以减少重复造轮子的时间。
    3.通过寻找，找到wechat-sdk，这个sdk把一些基本的微信常用方法进行了封装。
    4.微信接入的时候是使用get请求，而其他请求都是post请求，因此可以通过这一条件判断是首次接入还是其他请求，在post请求中处理相对应要实现的业务逻辑。
    5.网页授权获得用户信息根据微信公众api开发文档相关部分进行开发：
    
    第一步：用户同意授权，获取code
    第二步：通过code换取网页授权access_token
    第三步：刷新access_token（如果需要）
    第四步：拉取用户信息(需scope为 snsapi_userinfo)
    
[测试地址](https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx20c01c2975f7e07a&redirect_uri=http://www.m2ez.com/info/&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect "请用微信打开")

![测试微信号二维码](http://mmbiz.qpic.cn/mmbiz/bPe33PYsTH2lHgqIfp1gQlsa7piahnYtFQPKhgPricmaibKqpA33OHHTIm24eYOSicssHv4mxdFuoAY5f2ea8icrXJQ/0) 

