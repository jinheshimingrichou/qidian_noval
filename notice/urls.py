from django.urls import path,re_path
# 引入views.py
from . import views

app_name = 'notice'

urlpatterns = [
    # 通知列表

re_path(r'^personal/update/$', views.CommentNoticeUpdateView.as_view(), name='readed'),
re_path(r'^personal/message/$',views.Allmessages,name='message'),
]



