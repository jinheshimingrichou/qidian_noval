import json
import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from web import models
from django_redis import get_redis_connection

from utils.encrypt import uid



def index(request):
    return render(request, 'index.html')

