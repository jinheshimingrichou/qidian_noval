from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from web.models import *

def Allmessages(request):
    unnotices = Messages.objects.filter(receiver=request.noval.user).filter(is_read=False)
    notices = Messages.objects.filter(receiver=request.noval.user).filter(is_read=True)
    return render(request,'notice/message.html',{'unnotices':unnotices,'notices':notices})
# class CommentNoticeListView(ListView):
#     """通知列表"""
#     # 上下文的名称
#     context_object_name = 'notices'
#     # 模板位置
#     template_name = 'notice/message.html'
#
#     #重写init，赋予request。noval
#
#     def __init__(self, request, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.request = request
#     # 未读通知的查询集
#     @classmethod
#     def get_queryset(self):
#
#         return self.request.noval.user.notifications.unread()
# def msg_all_view(request):
#     msg_list = Messages.objects.filter(receiver = request.user)
#     return render(request, 'comment/msg_list.html',{'msg_list':msg_list})


# def msg_unread_view(request):
#
#     msg_list2 = []
#     for msg in msg_list:
#         if msg.is_read == False:
#             msg_list2.append(msg)
#
#     return render(request, 'comment/msg_list.html',{'msg_list':msg_list2})

class CommentNoticeUpdateView(View):
    """更新通知状态"""
    # 处理 get 请求
    def mark_all_as_read(self, recipient=None):
        queryset=Messages.objects.all()
        if  recipient:
            queryset = queryset.filter(receiver=recipient)
        for i in queryset:
            i.is_read=True
        return queryset.bulk_update(queryset,['is_read'])

    def mark_as_read(self,instance):
        if not instance.is_read:
            instance.is_read = True
            instance.save()

    def get(self, request):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        # 更新单条通知
        if notice_id:
            book = Books.objects.get(id=request.GET.get('book_id'))
            self.mark_as_read(Messages.objects.get(id=notice_id))
            return redirect(book)
        # 更新全部通知
        else:
            self.mark_all_as_read(request.noval.user)
            return redirect('notice:message')