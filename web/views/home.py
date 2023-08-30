import requests
from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.http import JsonResponse
from web.forms.account import *
from web.forms.comment import CommentForm
from utils.image_code import check_code
from django.db.models import Q,F
import uuid
import datetime
import json
def Lookbook(request):
    print('aaaaaaaaaaaaaaaaaaaaaaaaaa',request.user)

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
    # print('11111111111111111111111111111',book.myviewbook_set.filter())
    iscollection=MyViewBook.objects.filter(book=book,user=req.noval.user).first()
    if iscollection:
            iscollection=iscollection.collection
    comments = Comment.objects.filter(book=id)
    comment_form = CommentForm()
    return render(req, 'book_detail.html', {'iscollection':iscollection,"book":book,'comments':comments,'comment_form':comment_form})

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

from django.core import serializers
#500500500500,500
def Rank_tuijian(req):

    books = Books.objects.order_by('-recommend')[:10]
    return render(req, 'rank.html', {'books': books})
def Rank_yuepiao(req):
    books = Books.objects.order_by('-word')
    return render(req, 'rank.html', {'books': books})
def Rank_vipcollection(req):
    temp = Collections.objects.order_by('-coll_num')
    # print(temp)
    books=Books.objects.filter(prop=2).filter(id__in=temp.values('bookname')).order_by('-id')
    # print(books)
    return render(req, 'rank.html', {'books': books})

def Rank(req):
   books = Books.objects.order_by('-word')
   return render(req,'rank.html', {'books': books})
# def Rank(req):
#     data=req.GET.get('rank')
#     path=req.path_info.split('/')[-1]
#     print('danqian',path)
#     if not data:
#         books = Books.objects.order_by('-word')
#     else:
#         if path=='recommend':
#             print('yihuiqu')
#             books = Books.objects.order_by('-'+data)[:10]
#             return render(req, 'rank.html', {'books': books})
#         elif path=='vipcollection':
#             books = Books.objects.filter(prop=2).order_by('-'+data)
#         elif path=='yuepiao':
#             books = Books.objects.order_by('-word')
#         else:
#             return redirect('rank')
#         return render(req, 'rank.html', {'books': books})
#     return render(req, 'rank.html', {'books': books})

    # if req.POST.get('rank')=='yuepiao':
    #     books
    #     return JsonResponse()
    # if req.POST.get('rank')=='recommend':
    #     books = Books.objects.order_by('-recommend')
    #
    # if req.POST.get('rank')=='':


def End(req):
    books=Books.objects.filter(state=1)
    return render(req,'book_list.html',{'books':books})

def Free(req):
    books=Books.objects.filter(prop=1)
    return render(req,'book_list.html',{'books':books})

def Search(req):
    search=req.POST.get('search')
    books = Books.objects.filter(
        Q(name__icontains=search) |
        Q(author__name__icontains=search)
    )
    authors=Authors.objects.filter(name__icontains=search)
    print(authors)
    return render(req, 'search.html', {'books': books,'authors':authors})