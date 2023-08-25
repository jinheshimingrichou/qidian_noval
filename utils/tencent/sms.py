#!/usr/bin/env python
# -*- coding:utf-8 -*-


from qcloudsms_py import SmsMultiSender, SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

from django.conf import settings
from django.core.mail import send_mail

def send_email_single(email, template_id, template_param_list):
    """
    单条发送短信
    :param email:
    :param template_id: 腾讯云短信模板ID
    :param template_param_list: 短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
    :return:
    """
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

