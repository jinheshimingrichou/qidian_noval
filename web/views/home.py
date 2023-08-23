import requests
from django.shortcuts import render,HttpResponse, redirect
from django.http import JsonResponse
from web.forms.account import *
from utils.image_code import check_code
from django.db.models import Q,F
import uuid
import datetime
def Lookbook(request):
    books=Books.objects.all()
    # bb=Authors.objects.get(name='辰东')
    # cc=Books.objects.get(id=4)
    # print(bb.name,bb.books_set.all().first().name)
    # print(cc.author.name)
    # Authors.objects.all().update(book_total=F('book_total')+10)

    return render(request,'index.html', {"books":books,'type':' '})

# def index(request):
#
#     return render(request, 'index.html')

def Bookdetail(req,id):
    book = Books.objects.get(id=id)
    return render(req, 'book_detail.html', {"book":book})

def Authordetail(req,id):
    author = Authors.objects.get(id=id)
    books = Books.objects.filter(author=id)
    return render(req, 'author_detail.html', {"author":author,'books':books})

def Type(req,type):
    if type==' ':
        return redirect('index')
    books=Books.objects.all().filter(type=type)
    return render(req,'index.html',{'books':books})
def Category(req,category):
    books=Books.objects.all().filter(category=category)
    return render(req,'index.html',{'books':books})

def State(req,state):
    books=Books.objects.all().filter(state=state)
    return render(req,'index.html',{'books':books})

def Collection(req):
    CCC=Collections.objects.order_by('-coll_num')
    return render(req,'index.html',{'CCC':CCC})

def Popularity(req):
    books=Books.objects.order_by('-recommend')
    return render(req,'index.html',{'books':books})

def Word(req):
    books=Books.objects.order_by('-word')
    return render(req,'index.html',{'books':books})

def Rank(req):
    books=Books.objects.order_by('-word')
    return render(req,'rank.html',{'books':books})

def End(req):
    books=Books.objects.order_by('-word')
    return render(req,'book_list.html',{'books':books})

def Free(req):
    books=Books.objects.order_by('-word')
    return render(req,'book_list.html',{'books':books})