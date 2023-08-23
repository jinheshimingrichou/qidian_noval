import requests
from django.shortcuts import render,HttpResponse, redirect
from django.http import JsonResponse
from web.forms.account import *
from utils.image_code import check_code
from django.db.models import Q
import uuid
import datetime
from io import BytesIO
def register(request):
    # 注册
    if request.method=='GET':
        form = RegisterModelForm()
        return render(request, 'register.html',{'form':form})
    form = RegisterModelForm(data=request.POST)
    # print('lllllllllllllllllllll',request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status':True,'data':'/login/'})
    else:
        return JsonResponse({'status': False, 'error': form.errors})


def send_email(request):
    """ 发送短信 """
    print(request.GET)
    form = SendEmailForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})
    # return HttpResponse('ok')

    # 只是校验手机号：不能为空、格式是否正确


def login_email(request):
    """ 短信登录 """
    if request.method == 'GET':
        form = LoginEmailForm()
        return render(request, 'loginEmail.html', {'form': form})
    form = LoginEmailForm(request.POST)
    if form.is_valid():
        # 用户输入正确，登录成功
        email = form.cleaned_data['email']

        # 把用户名写入到session中
        user_object = UserInfo.objects.filter(email=email).first()
        request.session['user_id'] = user_object.id
        request.session.set_expiry(60 * 60 * 24 * 14)

        return JsonResponse({"status": True, 'data': "/index/"})

    return JsonResponse({"status": False, 'error': form.errors})



def login(request):
    """ 用户名和密码登录 """
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # user_object = models.UserInfo.objects.filter(username=username, password=password).first()
        #  (手机=username and pwd=pwd) or (邮箱=username and pwd=pwd)

        user_object = UserInfo.objects.filter(Q(email=username) | Q(username=username)).filter(
            password=password).first()
        if user_object:
            # 登录成功为止1
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)

            return redirect('index')

        form.add_error('username', '用户名或密码错误')

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """

    image_object, code = check_code()

    request.session['image_code'] = code
    request.session.set_expiry(60)  # 主动修改session的过期时间为60s

    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('index')