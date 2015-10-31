# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import hashlib

# index方法
def index(request):
    #获取微信传递参数
    signature   = request.GET.get('signature', None)
    timestamp   = request.GET.get('timestamp', None)
    nonce       = request.GET.get('nonce', None)
    echostr     = request.GET.get('echostr', None)
    #微信自己设置的token
    token       = 'life'
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
        return HttpResponse('weixin  index')
