# -*- coding: UTF-8 -*-

from django.shortcuts import render, redirect

from mainapp.globals import *
from .models import siteUsers
from .forms import regForm
from django.views.generic import View

import feedparser
import json

#from django.http import HttpResponse

# Create your views here.

#https://rus.azattyq.org/api/zqmtvek-tt

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

class UserCreate(View):

    def get(self, request):

        form = regForm()

        return render(request, 'account/newUser.html', context={'form': form})

    def post(self, request):

        bound_form = regForm(request.POST)

        if bound_form.is_valid():

            new = bound_form.save()

            return redirect(new)

        return render(request, 'account/newUser.html', context={'form': bound_form})
