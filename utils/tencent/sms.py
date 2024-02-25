#!/usr/bin/env python
# -*- coding:utf-8 -*-


from qcloudsms_py import SmsMultiSender, SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

from django.conf import settings
from django.core.mail import send_mail

def send_email_single(email, template_id, template_param_list):
    if template_id=='login':
        message = "您的登录验证码是【" + str(template_param_list)+ "】，10分钟内有效，请尽快填写"
    else:
        message = "您的注册验证码是【" + str(template_param_list) + "】，10分钟内有效，请尽快填写"
    emailBox = []
    emailBox.append(email)
    try:
        response=send_mail('终点中文网', message, '1454335861@qq.com', emailBox, fail_silently=False)
    except HTTPError as e:
        response = {'result': '1000', 'errmsg': "网络异常发送失败"}
    return response

