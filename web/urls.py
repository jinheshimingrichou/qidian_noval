"""
URL configuration for scrapy_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import re_path,path
from web.views import account,home
urlpatterns = [
    re_path(r'^register/$', account.register,name='register'),
re_path(r'^send/email/$', account.send_email,name='send_email'),
    re_path(r'^login/email/$', account.login_email, name='login_email'),
re_path(r'^login/$', account.login, name='login'),
re_path(r'^image/code/$', account.image_code, name='image_code'),
re_path(r'^index/$',home.index,name='index'),
re_path(r'^logout/$', account.logout, name='logout'),
    # path(r'^send/sms/', send_sms),
]
