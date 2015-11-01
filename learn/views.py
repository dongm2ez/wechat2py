# -*- coding: utf-8 -*-
import hashlib
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
                tmpStr = ''
                for key, value in userInfo.items():
                    tmpStr += "\"%s\":\"%s\"\"\n" % (key, value)
                response = wechat.response_text(tmpStr)
            else:
                response = wechat.response_text(u'回复【1】查看您的信息')
        return HttpResponse(response, content_type = "application/xml")
    else:
        return HttpResponse('')
