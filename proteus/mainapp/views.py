# -*- coding: UTF-8 -*-

from django.shortcuts import render

from mainapp.globals import *

from .models import Users

import feedparser
import pprint

#from django.http import HttpResponse

# Create your views here.

#https://rus.azattyq.org/api/zqmtvek-tt

import json

def index(request):
    return render(request, 'index.html', {'values': site})

def auth(request):
    return render(request, 'auth.html', {'values': site})

def last(request):

    rss = 'https://rus.azattyq.org/api/zqmtvek-tt'
    feed = feedparser.parse(rss)

    return render(request, 'last.html', {'feed': feed, 'values': site})

def reg(request):

    return render(request, 'register.html', {'all': Users.objects.all(), 'request': request.POST, 'values': site})
