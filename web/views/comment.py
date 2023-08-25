from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, JsonResponse

from web.forms.comment import CommentForm
from web.models import *

# from notifications.signals import notify
# from django.contrib.auth.models import User

# 文章评论, parent_comment_id=None

def Comment(request, book_id=1):
    # if request.method == 'GET':
    #     form = CommentForm()
    #     context = {
    #         'comment_form': form,
    #         'book_id': book_id,
    #         'parent_comment_id': None
    #     }
    #     return render(request, 'comment/reply.html', context)
    # print(request.POST)
    if request.method == 'GET':
        form = CommentForm()
        context = {
                'comment_form': form,
                'book_id': book_id,
            }
        return render(request, 'comment.html', context)
    book = get_object_or_404(Books, id=book_id)
    form = CommentForm(request.POST)
    if form.is_valid():

        comment = form.save(commit=False)
        comment.content=request.POST.get('content')
        comment.book = book
        comment.user = request.noval.user
        print(comment,comment.content,comment.book,comment.user)

        # # 二级回复
        # if parent_comment_id:
        #     parent_comment = Comment.objects.get(id=parent_comment_id)
        #     # 若回复层级超过二级，则转换为二级
        #     comment.parent_id = parent_comment.get_root().id
        #     # 被回复人
        #     comment.reply_to_id = parent_comment.user
        #     comment.save()
        #     return HttpResponse("200 OK")
            # return JsonResponse({"code": "200 OK", "comment_id": comment.id})

        comment.save()
        # 添加锚点
        # redirect_url = book.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
        return HttpResponse('ollllkkk')
    else:
        return JsonResponse({'status': False, 'error': form.errors})

