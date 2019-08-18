# -*- coding: UTF-8 -*-

from django.shortcuts import render, redirect

from mainapp.globals import *
from .models import siteUsers, rssPosts
from .forms import regForm
from django.views.generic import View

import feedparser, json, hashlib

#from django.http import HttpResponse

# Create your views here.

rss = 'https://rus.azattyq.org/api/zrqomeuuo_'

def index(request):
    return render(request, 'index.html', {'values': site})

def auth(request):
    return render(request, 'auth.html', {'values': site})

def popularTags(request):

    feed = feedparser.parse(rss)

    updatePosts(feed)

    return render(request, 'popularTags.html', {'feed': feed, 'values': site})

def tags(request, slug):

    slugs = slug.replace('-', ' ').lower()
    feed = feedparser.parse(rss)

    arr = slugs.split('&')

    updatePosts(feed)

    tag_names = dict()

    for post in feed['items']:

        for tag in post['tags']: tag_names.update({tag['term'].lower(): hashlib.sha224(post['summary'].encode('utf-8')).hexdigest()})

    new = []

    for slug in arr:

        if(slug in tag_names.keys()):

            for post in feed['items']:

                tag_names = dict()

                for tag in post['tags']: tag_names.update({tag['term'].lower(): hashlib.sha224(post['summary'].encode('utf-8')).hexdigest()})

                if slug in tag_names:

                    new.append({})

                    for key in post.keys():

                        new[len(new)-1].update({key: post[key]})

    return render(request, 'tags.html', {'feed': new, 'values': site})

def find(request):

    slug = request.GET.get('search', default='Мир').lower()
    feed = feedparser.parse(rss)

    updatePosts(feed)

    tag_names = dict()

    for post in feed['items']:

        for tag in post['tags']: tag_names.update({tag['term'].lower(): hashlib.sha224(post['summary'].encode('utf-8')).hexdigest()})

    new = []

    if(slug in tag_names.keys()):

        for post in feed['items']:

            tag_names = dict()

            for tag in post['tags']: tag_names.update({tag['term'].lower(): hashlib.sha224(post['summary'].encode('utf-8')).hexdigest()})

            if slug in tag_names:

                new.append({})

                for key in post.keys():

                    new[len(new)-1].update({key: post[key]})

    return render(request, 'tags.html', {'feed': new, 'values': site})

def updatePosts(feed):

    for post in feed['items']:

        token = hashlib.sha224(post['summary'].encode('utf-8')).hexdigest()

        try:
            rssPosts.objects.get(token=token)

        except rssPosts.DoesNotExist:
            new = rssPosts(token=token)
            new.save()

def last(request):

    feed = feedparser.parse(rss)

    updatePosts(feed)

    return render(request, 'last.html', {'feed': feed, 'values': site})

def reg(request):

    return render(request, 'register.html', {'all': Users.objects.all(), 'request': request.POST, 'values': site})

class UserCreate(View):

    def get(self, request):

        form = regForm()

        return render(request, 'auth.html', context={'form': form})

    def post(self, request):

        bound_form = regForm(request.POST)

        if bound_form.is_valid():

            new = bound_form.save()

            return redirect(new)

        return render(request, 'auth.html', context={'form': bound_form})
