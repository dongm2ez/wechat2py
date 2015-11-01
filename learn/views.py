# -*- coding: utf-8 -*-
import hashlib
import urllib
import urllib2
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage

TOKEN = 'life'
AppID = 'wx20c01c2975f7e07a'
AppSecret = 'd4624c36b6795d1d99dcf0547af5443d'

# 实例化 wechat
wechat = WechatBasic(token = TOKEN, appid = AppID, appsecret = AppSecret)

@csrf_exempt
def index(request):
    if request.method == 'GET':
        #获取微信传递参数
        signature   = request.GET.get('signature', None)
        timestamp   = request.GET.get('timestamp', None)
        nonce       = request.GET.get('nonce', None)
        echostr     = request.GET.get('echostr', None)
        #微信自己设置的token
        token       = TOKEN
        #将token、timestamp、nonce三个参数进行字典序排序
        tmpList     = [token, timestamp, nonce]
        tmpList.sort()
        #将三个参数字符串拼接成一个字符串进行sha1加密
        tmpStr      = "%s%s%s" % tuple(tmpList)
        hashcode    = hashlib.sha1(tmpStr).hexdigest()
        #如果是来自微信请求，则回复echostr
        if hashcode == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('wechat  index')
    elif request.method == 'POST':
        # 解析本次xml数据
        try:
            wechat.parse_data(data = request.body)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')
        # 获取解析好的xml数据
        message = wechat.get_message()
        # 关注事件或者默认不匹配回复内容
        response = wechat.response_text(u'感谢您的关注！')
        # 类型是文字回复内容
        if message.type == 'text':
            if message.content == '1':
                openid   = message.source
                userInfo = wechat.get_user_info(openid)
                tmpStr   = ''
                for key, value in userInfo.items():
                    tmpStr += "%s:%s\n" % (key, value)
                response = wechat.response_text(tmpStr)
            elif message.content == '2':
                # 网页授权获得用户信息
                oauth_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + AppID + "&redirect_uri=http://www.m2ez.com/info/&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
                response = wechat.response_text(oauth_url)
            else:
                response = wechat.response_text(u'回复【1】查看您的信息\n回复【2】网页授权获得信息')
        return HttpResponse(response, content_type = "application/xml")
    else:
        return HttpResponse('')

def info(request):
    # 获取微信返回的code
    code = request.GET.get('code', None);
    accessTokenUrl = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=" + AppID + "&secret=" + AppSecret + "&code=" + code + "&grant_type=authorization_code"
    # 获取网页返回信息
    req         = urllib2.Request(accessTokenUrl)
    resData     = urllib2.urlopen(req)
    res         = resData.read()
    # access_token转换为字典
    accessDict  = eval(res)
    userInfoUrl = "https://api.weixin.qq.com/sns/userinfo?access_token=" + accessDict['access_token'] + "&openid=" + accessDict['openid'] + "&lang=zh_CN"
    # 获取网页返回信息
    req         = urllib2.Request(userInfoUrl)
    resData     = urllib2.urlopen(req)
    res         = resData.read()
    # 用户信息转换为字典
    userInfoDict  = eval(res)
    tmpStr   = ''
    for key, value in userInfoDict.items():
        tmpStr += "<h1>%s:%s</h1>" % (key, value)
    return HttpResponse(tmpStr)