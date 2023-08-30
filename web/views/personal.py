import requests
from django.shortcuts import render,HttpResponse, redirect
from django.http import JsonResponse
from web.forms.baseinfo import *
from web.forms.comment import CommentForm
from utils.image_code import check_code
from django.db.models import Q,F
import uuid
import datetime
import os
from scrapy_django import settings
from django.views import View
from django.http import QueryDict
def FirstPage(request):
    user=BaseInfo.objects.get(name=request.noval.user)
    print(user)
    return render(request,'personal.html', {'user':user})



# def (request):
#     if request.method=='GET':
#         books=MyViewBook.objects.filter(user=request.noval.user)
#         return render(request,'',{'books':books})
#

class BookShelf(View):
    def get(self,request):#查
        books = MyViewBook.objects.filter(user=request.noval.user)
        return render(request,'bookshelf.html', {'books': books})

    def post(self,request):#增
        try:
            id = request.POST.get('id')
            book=Books.objects.get(id=id)
            if not MyViewBook.objects.filter(book=book).exists():
                MyViewBook.objects.create(
                    user=request.noval.user,
                book=book,
                collection=True,
                time=datetime.datetime.now())
                #收藏数增加

                return JsonResponse({'state':200,'data':'添加成功'})
        except Exception as e:
            return JsonResponse({'state':500,'data':e})


    def delete(self, request):  # 删
        try:
            DELETE = QueryDict(request.body)
            id = DELETE.get('id')
            # book = Books.objects.filter(id=id).first()
            the=MyViewBook.objects.filter(book=id)

            if  the.exists():
                the.update(collection=False)
                the.delete()
                return JsonResponse({'state': 200, 'data': '删除成功'})
            return JsonResponse({'state': 200, 'data': 'buunzai'})
        except Exception as e:
            return JsonResponse({'state': 500, 'data':e })






def Message(request):

   return render(request, 'notice/message.html')



class Settings(View):
    template_name='setting.html'

    def get(self,request, id):
        baseinfo=BaseInfo.objects.filter(id=id).first()
        default_data = {'sex':baseinfo.sex,
                        'introduction':baseinfo.introduction,'gory':baseinfo.gory}
        form = BaseInfoModelForm(default_data)
        form.icon=baseinfo.icon

        for i in form:
            print(i)
        return render(request,self.template_name,{'form':form,'icon':baseinfo.icon,'id':id})

    def post(self,request,id):
        baseinfo = BaseInfo.objects.filter(id=id).first()
        form=BaseInfoModelForm(request.POST, request.FILES)
        if form.is_valid():
            newdata=form.cleaned_data
            baseinfo.sex =newdata['sex']
            baseinfo.gory=newdata['gory']
            baseinfo.introduction=newdata['introduction']
            picture = request.FILES.get('icon')
            file_name = baseinfo.name.username + '.jpg'
            file_path = os.path.join(settings.MEDIA_ROOT + 'user/', file_name)
            with open(file_path, 'ab') as fp:
                for part in picture.chunks():
                    fp.write(part)
                    fp.flush()
            baseinfo.icon = 'user/' + file_name

            baseinfo.save()
        return redirect('firstpage')
