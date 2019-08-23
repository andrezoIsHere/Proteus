# -*- coding: UTF-8 -*-

from django.shortcuts import render, redirect

from mainapp.globals import *
from .models import siteUsers, rssPosts
from .forms import newForm, loginForm
from django.views.generic import View
#from django.contrib.auth import logout
from django.http import HttpResponseRedirect

import feedparser, json, hashlib

from django.http import HttpResponse

# Create your views here.

#rss = 'https://rus.azattyq.org/api/zrqomeuuo_'
#rss2 = 'https://rus.azattyq.org/api/zororegtor'

def checkRss(cooks):

    try:

        if not cooks['rss-client']: return 'https://rus.azattyq.org/api/zrqomeuuo_'
        else: return cooks['rss-client']

    except:

        return 'https://rus.azattyq.org/api/zrqomeuuo_'

def set_global_url(request):

    rss = checkRss(request.COOKIES)

    try:

        if request.GET:

            if request.GET.get('url'):

                response = HttpResponse()
                response.set_cookie(key='rss-client', value=request.GET.get('url'), expires=99999999)

                response.write('true')

                return response

        else: return HttpResponse('Server returned bad result')

    except:

        return HttpResponse('Server returned bad result')

def account(request):

    rss = checkRss(request.COOKIES)

    try:
        if not request.COOKIES['login']: return redirect(auth)

    except:
        return redirect(auth)

    return render(request, 'account.html', {'values': site, 'tags': popularTags(request)})

def index(request):

    rss = checkRss(request.COOKIES)

    feed = getFeed(request)

    return render(request, 'index.html', {'values': site, 'feed': feed, 'tags': popularTags(request)})

def auth(request):

    rss = checkRss(request.COOKIES)

    try:
        if request.COOKIES['login']: return redirect(last)
    except:
        print('User tried to enter in auth page with saved cookies')

    if request.method == 'GET':

        newUserForm = newForm()

        loginUserForm = loginForm()

        return render(request, 'auth.html', {'values': site, 'loginuser': loginUserForm, 'newuser': newUserForm, 'tags': popularTags(request)})

    elif request.method == 'POST' and request.POST.get('type') == 'newuser':

        dct = {}

        for object in request.POST:

            if object.find('-') >= 0:

                if str(object.split('-')[0]) == 'newuser':

                    dct.update({str(object.split('-')[1]): str(request.POST.get(object))})

        bound_form = newForm(dct)

        if bound_form.is_valid():

            try:

                request.session['user-info'] = {}

                another = siteUsers.objects.filter(login=bound_form.cleaned_data['login'])

                if another[0].login:

                    return render(request, 'auth.html', {'feed': getFeed(request), 'saved': bound_form.cleaned_data, 'newuser': bound_form, 'values': site, 'tags': popularTags(request)})

            except:

                new_user = bound_form.save()

                request.session['user-info'] = {}

                response = redirect(last)

                response.set_cookie(key='login', value=bound_form.cleaned_data['login'], expires=99999999);
                response.set_cookie(key='password', value=hashlib.sha224(bound_form.cleaned_data['password'].encode('utf-8')).hexdigest(), expires=99999999);
                response.set_cookie(key='email', value=bound_form.cleaned_data['email'], expires=99999999);

                return response

        return render(request, 'auth.html', {'feed': getFeed(request), 'saved': bound_form.cleaned_data, 'newuser': bound_form, 'values': site, 'tags': popularTags(request)})

    elif request.method == 'POST' and request.POST.get('type') == 'loginuser':

        dct = {}

        dct.update({'login': str(request.POST.get('loginuser-login'))})
        dct.update({'password': str(request.POST.get('loginuser-password'))})

        bound_form = loginForm(dct)

        if bound_form.is_valid():

            new_user = bound_form.save()

            response = redirect(last)

            response.set_cookie(key='login', value=dct['login'], expires=99999999);
            response.set_cookie(key='password', value=hashlib.sha224(dct['password'].encode('utf-8')).hexdigest(), expires=99999999);

            return response

        return render(request, 'auth.html', {'feed': getFeed(request), 'saved': bound_form.cleaned_data, 'loginuser': bound_form, 'values': site, 'tags': popularTags(request)})

def popular(request):

    rss = checkRss(request.COOKIES)

    if request.COOKIES.get('login') and request.COOKIES.get('password'):

        feed = getFeed(request)
        pop = popularPosts(request, feed)

        parsed = {}

        for post in feed['items']:

            parsed.update({hashlib.sha224(post['summary'].encode('utf-8')).hexdigest(): post})

        sortedarr = sorted(pop.items(), key=lambda kv: kv[1][0], reverse=True)

        return render(request, 'popular.html', {'feed': sortedarr, 'values': site, 'tags': popularTags(request)})

    else: return redirect(auth)

def exit(request):

    rss = checkRss(request.COOKIES)

    cooks = request.COOKIES
    response = HttpResponseRedirect('index')

    for obj in cooks: response.delete_cookie(obj)

    return response

def filter_feed(request):

    rss = checkRss(request.COOKIES)

    if request.GET.get('filter') == 'tags':
        print('bad')

def get_reaction(request):

    rss = checkRss(request.COOKIES)

    res = {}

    response = HttpResponse()

    try:
        result = rssPosts.objects.get(token=request.GET['token'])
        res.update({'likes': result.likes, 'dislikes': result.dislikes, 'views': result.views})

        response.write(json.dumps({'likes': result.likes, 'dislikes': result.dislikes, 'views': result.views}))

    except:
        res.update({'likes': 0, 'dislikes': 0, 'views': 0})

        response.write(json.dumps({'likes': 0, 'dislikes': 0, 'views': 0}))

    return response

def add_view(request):

    rss = checkRss(request.COOKIES)

    try:

        if request.COOKIES:

            if request.COOKIES.get(hashlib.sha224(request.GET['token'].encode('utf-8')).hexdigest()) != 'viewed':

                result = rssPosts.objects.get(token=request.GET['token'])

                response = HttpResponse()

                response.set_cookie(hashlib.sha224(request.GET['token'].encode('utf-8')).hexdigest(), 'viewed', expires=99999999)

                result.views += 1

                result.save()

                return response

            else:

                response = HttpResponse(json.dumps({'error': {'errornum': 1003, 'errortext': "You can't do it more than 2 times"}}))

                return response

        else:

            response = HttpResponse()

            response.set_cookie(hashlib.sha224(request.GET['token'].encode('utf-8')).hexdigest(), 'viewed', expires=99999999)

            result = rssPosts.objects.get(token=request.GET['token'])

            result.views += 1

            result.save()

            return response

    except:

        response = HttpResponse(json.dumps({'error': {'errornum': 1004, 'errortext': "Not full input"}}))

        return response

def set_reaction(request):

    rss = checkRss(request.COOKIES)

    token = request.GET['token']
    reaction_type = request.GET['type']

    if token and reaction_type:

        if type(token) == str and type(reaction_type) == str:

            result = True

            try:

                getReactions = userReactions.objects.get(login=request.COOKIES.get('login'),token=token)

                if getReactions['reaction'] == reaction_type: result = False

                else: result = True

            except:

                '''user = {'login': request.COOKIES.get('login'), 'reaction': reaction_type, 'posttoken': token}

                print(user)

                reactionSet = newReaction(user)

                if reactionSet.is_valid(): reactionSet.save()'''

                result = True

            try:

                if rssPosts.objects.get(token=token) and result:

                    plus = ''

                    post = rssPosts.objects.get(token=token)

                    response = HttpResponse()

                    #like
                    if reaction_type == 'like':

                        if request.COOKIES.get(token) == 'like':

                            response = HttpResponse(json.dumps({'error': {'errornum': 1003, 'errortext': "You can't do it more than 2 times"}}))

                            return response

                            plus = 'like'

                        else:

                            post.likes += 1

                            response.set_cookie(token, 'like', expires=99999999)

                            if post.dislikes > 0: post.dislikes -= 1
                            else: post.dislikes = 0

                            plus = 'like'

                    #dislike
                    else:

                        if request.COOKIES.get(token) == 'dislike':

                            response = HttpResponse(json.dumps({'error': {'errornum': 1003, 'errortext': "You can't do it more than 2 times"}}))

                            return response

                            plus = 'dislike'

                        else:

                            if post.likes > 0: post.likes -= 1
                            else: post.likes = 0

                            response.set_cookie(token, 'dislike', expires=99999999)

                            post.dislikes += 1

                            plus = 'dislike'

                    response.write(json.dumps({'result': {'likes': post.likes, 'dislikes': post.dislikes, 'plus': plus}}))

                    post.save()

                    return response

                else:

                    response = HttpResponse(json.dumps({'error': {'errornum': 1003, 'errortext': "You can't do it more than 2 times"}}))

                    return response

            except Exception:

                response = HttpResponse(json.dumps({'error': {'errornum': 1004, 'errortext': 'Accessing a nonexistent item'}}))

                return response

        else:

            response = HttpResponse(json.dumps({'error': {'errornum': 1002, 'errortext': 'Incorrect input'}}))

            return response

    else:

        response = HttpResponse(json.dumps({'error': {'errornum': 1001, 'errortext': 'Not full input'}}))

        return response

def popularPosts(request, feed):

    rss = checkRss(request.COOKIES)

    res = {}

    for post in feed['items']:

        token = hashlib.sha224(post['summary'].encode('utf-8')).hexdigest()

        try:
            result = rssPosts.objects.get(token=token)

            if int(result.views) == 0:

                res.update({token:
                    [(int(result.likes) - int(result.dislikes)) * 1, [post, getPostInfo(request, token)]]
                })

            else:

                res.update({token:
                    [(int(result.likes) - int(result.dislikes)) * int(result.views), [post, getPostInfo(request, token)]]
                })

        except rssPosts.DoesNotExist:
            new = rssPosts(token=token)
            new.save()

            result = rssPosts.objects.get(token=token)

            if int(result.views) == 0:

                res.update({token:
                    [(int(result.likes) - int(result.dislikes)) * 1, [post, getPostInfo(request, token)]]
                })

            else:

                res.update({token:
                    [(int(result.likes) - int(result.dislikes)) * int(result.views), [post, getPostInfo(request, token)]]
                })

    return res

def getFeed(request):

    rss = checkRss(request.COOKIES)

    feed = feedparser.parse(rss)

    updatePosts(request, feed)

    return feed

def popularTags(request):
    
    rss = checkRss(request.COOKIES)

    feed = feedparser.parse(rss)

    updatePosts(request, feed)

    tag_names = dict()

    for post in feed['items']:

        for tag in post['tags']: tag_names.update({tag['term']: hashlib.sha224(post['summary'].encode('utf-8')).hexdigest()})

    get = []

    for key in tag_names.keys():
        get.append(key)

    return get

def tags(request, slug):

    rss = checkRss(request.COOKIES)

    slugs = slug.replace('-', ' ').lower()
    feed = feedparser.parse(rss)

    arr = slugs.split('&')

    updatePosts(request, feed)

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

    return render(request, 'tags.html', {'feed': new, 'values': site, 'tags': popularTags(request)})

def find(request):

    rss = checkRss(request.COOKIES)

    slug = request.GET.get('search', default='Мир').lower()
    feed = feedparser.parse(rss)

    updatePosts(request, feed)

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

    return render(request, 'tags.html', {'feed': new, 'values': site, 'tags': popularTags(request)})

def getPostInfo(request, token):

    rss = checkRss(request.COOKIES)

    res = {}

    try:
        result = rssPosts.objects.get(token=token)
        res.update({'likes': result.likes, 'dislikes': result.dislikes, 'views': result.views})
    except:
        res.update({'likes': 0, 'dislikes': 0, 'views': 0})

    return res

def updatePosts(request, feed):

    rss = checkRss(request.COOKIES)

    for post in feed['items']:

        token = hashlib.sha224(post['summary'].encode('utf-8')).hexdigest()

        try:
            rssPosts.objects.get(token=token)

        except rssPosts.DoesNotExist:
            new = rssPosts(token=token)
            new.save()

def last(request):

    rss = checkRss(request.COOKIES)

    feed = feedparser.parse(rss)

    updatePosts(request, feed)

    return render(request, 'last.html', {'feed': feed, 'values': site, 'tags': popularTags(request)})

