#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from web.models import *


class Noval(object):

    def __init__(self):
        self.user = None



class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """ 如果用户已登录，则request中赋值 """

        request.noval = Noval()

        user_id = request.session.get('user_id', 0)
        user_object = UserInfo.objects.filter(id=user_id).first()
        request.noval.user = user_object

        # 白名单：没有登录都可以访问的URL
        """
        1. 获取当用户访问的URL
        2. 检查URL是否在白名单中，如果再则可以继续向后访问，如果不在则进行判断是否已登录
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        # 检查用户是否已登录，已登录继续往后走；未登录则返回登录页面。
        if not request.noval.user:
            return redirect('login')

        # 登录成功之后，访问后台管理时：获取当前用户所拥有的额度

        # 方式一：免费额度在交易记录中存储

        # 获取当前用户ID值最大（最近交易记录）
        # _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
        # # 判断是否已过期
        # current_datetime = datetime.datetime.now()
        # if _object.end_datetime and _object.end_datetime < current_datetime:
        #     _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()
        #
        # request.tracer.price_policy = _object.price_policy

        # 方式二：免费的额度存储配置文件
        """
        # 获取当前用户ID值最大（最近交易记录）
        _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()

        if not _object:
            # 没有购买
            request.price_policy = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
        else:
            # 付费版
            current_datetime = datetime.datetime.now()
            if _object.end_datetime and _object.end_datetime < current_datetime:
                request.price_policy = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
            else:
                request.price_policy = _object.price_policy
        """

    def process_view(self, request, view, args, kwargs):

        # 判断URL是否是以manage开头，如果是则判断项目ID是否是我创建 or 参与
        if not request.path_info.startswith('/manage/'):
            return

        project_id = kwargs.get('project_id')
        # 是否是我创建的
        project_object = models.Project.objects.filter(creator=request.tracer.user, id=project_id).first()
        if project_object:
            # 是我创建的项目的话，我就让他通过
            request.tracer.project = project_object
            return

        # 是否是我参与的项目
        project_user_object = models.ProjectUser.objects.filter(user=request.tracer.user, project_id=project_id).first()
        if project_user_object:
            # 是我参与的项目
            request.tracer.project = project_user_object.project
            return

        return redirect('project_list')
