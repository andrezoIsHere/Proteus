# -*- coding: UTF-8 -*-

from django.shortcuts import render

from mainapp.globals import *

#from django.http import HttpResponse

# Create your views here.

#https://rus.azattyq.org/api/zqmtvek-tt

def index(request):
    return render(request, 'index.html', {'values': site})
