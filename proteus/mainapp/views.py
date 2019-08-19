# -*- coding: UTF-8 -*-

from django.shortcuts import render, redirect

from mainapp.globals import *
from .models import siteUsers, rssPosts
from .forms import newForm
from django.views.generic import View

import feedparser, json, hashlib

#from django.http import HttpResponse

# Create your views here.

rss = 'https://rus.azattyq.org/api/zrqomeuuo_'

def index(request):
    return render(request, 'index.html', {'values': site, 'tags': popularTags()})

def auth(request):

    if request.method == 'GET':

        newUserForm = newForm()

        return render(request, 'auth.html', {'values': site, 'newuser': newUserForm, 'tags': popularTags()})

    elif request.method == 'POST':

        dct = {}

        for object in request.POST:

            if object.find('-') >= 0:

                print('\n\n' + str(object.split('-')[0]))

                if str(object.split('-')[0]) == 'newuser': dct.update({str(object.split('-')[1]): str(request.POST.get(object))})

        print(dct)

        bound_form = newForm(dct)

        if bound_form.is_valid():

            new_user = bound_form.save()
            return redirect(last)

        return render(request, 'auth.html', {'feed': getFeed(), 'saved': bound_form.cleaned_data, 'newuser': bound_form, 'values': site, 'tags': popularTags()})

def getFeed():

    feed = feedparser.parse(rss)

    updatePosts(feed)

    return feed

def popularTags():

    feed = feedparser.parse(rss)

    updatePosts(feed)

    tag_names = dict()

    for post in feed['items']:

        for tag in post['tags']: tag_names.update({tag['term']: hashlib.sha224(post['summary'].encode('utf-8')).hexdigest()})

    get = []

    for key in tag_names.keys():
        get.append(key)

    return get

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

    return render(request, 'tags.html', {'feed': new, 'values': site, 'tags': popularTags()})

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

    return render(request, 'tags.html', {'feed': new, 'values': site, 'tags': popularTags()})

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

    return render(request, 'last.html', {'feed': feed, 'values': site, 'tags': popularTags()})

'''def reg(request):

    return render(request, 'register.html', {'all': Users.objects.all(), 'request': request.POST, 'values': site, 'tags': popularTags()})'''
