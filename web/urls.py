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
re_path(r'^index/$',home.Lookbook,name='index'),
re_path(r'^logout/$', account.logout, name='logout'),
re_path(r'^book/(?P<id>\d+)$', home.Bookdetail, name='book_detail'),
re_path(r'^author/(?P<id>\d+)$', home.Authordetail, name='author_detail'),
# ,path('book/<str:id>',home.Bookdetail,name='book_detail')
    # path(r'^send/sms/', send_sms),path('detail/<str:name>',Bookdetail,name='detail'),
path('type/<str:type>',home.Type,name='type'),
path('category/<str:category>',home.Category,name='category'),
path('state/<str:state>',home.State,name='state'),
re_path(r'^collection/$',home.Collection,name='collection'),
re_path(r'^popularity/$',home.Popularity,name='popularity'),
re_path(r'^word/$',home.Word,name='word'),
re_path(r'^rank/$',home.Rank,name='rank'),
re_path(r'^end/$',home.End,name='end'),
re_path(r'^free/$',home.Free,name='free'),
]
