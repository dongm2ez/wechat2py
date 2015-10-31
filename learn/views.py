# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import hashlib

# index方法
def index(request):
    #获取微信传递参数
    signature = request.GET['signature']
    timestamp = request.GET['timestamp']
    nonce     = request.GET['nonce']
    echostr   = request.GET['echostr']
    #微信自己设置的token
    token     = 'life'
    #字典排序
    list      = [signature, timestamp, nonce]
    list.sort()
    sha1      = hashlib.sha1()
    map(sha1.update, list)
    hashcode  = sha1.hexdigest()
    #sha1加密算法

    #如果是来自微信请求，则回复echostr
    if hashcode == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse('')
