"""proteus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
#from django.urls import path
from django.conf.urls import include, url
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url('index', views.index, name='index'),
    url('tags/(?P<slug>[\w-]+)', views.tags, name='tags'),
    url('filter_feed', views.filter_feed, name="filter_feed"),
    url('exit', views.exit, name="exit"),
    url('set_reaction', views.set_reaction, name="set_reaction"),
    url('get_reaction', views.get_reaction, name="get_reaction"),
    url('add_view', views.add_view, name="add_view"),
    url('popular', views.popular, name='popular'),
    url('find', views.find, name='find'),
    url('auth', views.auth, name='auth'),
    url('last', views.last, name='last'),
    url('', views.index, name='index')
]

urlpatterns += staticfiles_urlpatterns()
