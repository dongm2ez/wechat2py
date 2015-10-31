# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

# index方法
def index(request):
    return HttpResponse('Hello world')
