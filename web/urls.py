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
from django.urls import re_path,path,include
from web.views import account,home,comment,personal
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve # 导入媒体文件资源
urlpatterns = [
    re_path(r'^register/$', account.register,name='register'),
re_path(r'^send/email/$', account.send_email,name='send_email'),
    re_path(r'^login/email/$', account.login_email, name='login_email'),
re_path(r'^login/$', account.Login, name='login'),
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

# re_path(r'^rank/(?P<url>\w+)/$',home.Rank,name='rank'),
re_path(r'^rank/word$',home.Rank,name='rank'),
re_path(r'^rank/recommend/$',home.Rank_tuijian,name='tuijian'),
re_path(r'^rank/yuepiao/$',home.Rank_yuepiao,name='yuepiao'),
re_path(r'^rank/vipcollection$',home.Rank_vipcollection,name='vipcollection'),

re_path(r'^end/$',home.End,name='end'),
re_path(r'^free/$',home.Free,name='free'),

re_path(r'^search/$',home.Search,name='search'),

    path('comment/<int:book_id>',comment.Comments , name='comment'),
    re_path(r'^reply/(?P<book_id>\d+)/(?P<parent_comment_id>\d+)/$', comment.Comments, name='reply'),
    # path('reply/<int:book_id>/<int:parent_comment_id>', comment.Comment, name='reply'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # 图片文件路径，这里要注意，之前已经在setting.py文件处设置了媒体文件路径的别名是：MEDIA_URL = "/files/" ，所以这里的路由要保持一致




re_path(r'^personal/firstpage/$',personal.FirstPage,name='firstpage'),
# re_path(r'^personal/bookshelf/$',personal.BookShelf,name='bookshelf'),
re_path(r'^personal/bookshelf/$',personal.BookShelf.as_view(),name='bookshelf'),




re_path(r'^setting/(?P<id>\d+)$',personal.Settings.as_view(),name='setting'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)