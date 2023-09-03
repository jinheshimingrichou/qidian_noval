from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, JsonResponse

from web.forms.comment import CommentForm
from web.models import *
from notifications.signals import notify
from django.db.models.signals import post_save
from notifications.signals import notify
from web.models import UserInfo
from django.db.models import Q,F
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Comment) #只接收comment发来的post_save消息
def create_msg_handler(sender, instance, **kwargs):
    # content = instance.comment  # instance 就是发信号的对象，这里是个评论
    if instance.parent_id:
        sender = instance.user     # 获取评论者，即消息发送者
        receiver = instance.reply_to   # 通知文章作者
        msg = Messages(sender=sender, receiver=receiver, comment=instance)  # 新建消息保存
        msg.save()
def my_handler(sender, instance, book, acomment, **kwargs):
    try:
        notify.send(
            sender=sender,  # 评论者
            recipient=instance,  # 被回复者
            verb='回复了你',
            target=book,
            action_object=acomment,
        )
    except Exception as e:
        print(e)


# from notifications.signals import notify
# from django.contrib.auth.models import User
from django.contrib.auth.models import User
# 文章评论, parent_comment_id=None
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def Comments(request, book_id, parent_comment_id=None):
    book = get_object_or_404(Books, id=book_id)
    if request.method == 'GET':
        form = CommentForm()
        context = {
            'comment_form': form,
            'book_id': book_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    print(request.POST)
    # if request.method == 'GET':
    #     form = CommentForm()
    #     context = {
    #             'comment_form': form,
    #             'book_id': book_id,
    #         }
    #     return render(request, 'comment.html', context)
    form = CommentForm(request.POST)
    if form.is_valid():
        acomment = form.save(commit=False)
        acomment.content = request.POST.get('content')
        acomment.book = book
        acomment.user = request.noval.user
        # print(comment,comment.content,comment.book,comment.user)

        # 二级回复
        if parent_comment_id:
            print(parent_comment_id)
            parent_comment = Comment.objects.get(id=parent_comment_id)
            # 若回复层级超过二级，则转换为二级
            acomment.parent_id = parent_comment.get_root().id
            # 被回复人
            acomment.reply_to = parent_comment.user
            acomment.save()

            # 新增代码，给其他用户发送通知
            # 给其他用户发送通知
            # print(isinstance(parent_comment.user,request.noval.user))
            # print('fupinglu', request.user, 'zipingl', request.noval.user)
            # if parent_comment.user == request.user:
            # #     notify.send(request.user,#评论者recipient=parent_comment.user,#被回复者verb='回复了你',target=book,action_object=acomment,)
            #     post_save.connect(, sender=request.noval.user,
            #                       instance=parent_comment.user,
            #                       book=book,
            #                       acomment=acomment)
            #     recipient = request.noval.user
            #     # notify.send(recipient, recipient, verb='New Contact us request')
            #     print('xioaxiokok')
            # # return HttpResponse("200 OK")
            return JsonResponse({"code": "200 OK", "comment_id": acomment.id})

        acomment.save()

        # 添加锚点
        redirect_url = book.get_absolute_url() + '#comment_elem_' + str(acomment.id)
        print('rrrrrrrrrrrrrrrrrrrrrr', redirect_url)
        return redirect(redirect_url)
    else:
        return JsonResponse({'status': False, 'error': form.errors})


def my_book_comm(request):
    comments=Comment.objects.filter(Q(parent_id=None)&Q(user=request.noval.user))
    return render(request,'comment/my_book_comm.html',{'comments':comments})