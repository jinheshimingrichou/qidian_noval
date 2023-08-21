from django import forms
from web.models import *
from utils import encrypt
from web.forms.bootstrap import BootStrapForm
from django_redis import get_redis_connection
from django.core.exceptions import ValidationError
from utils.tencent.sms import send_email_single
import random
class RegisterModelForm(BootStrapForm,forms.ModelForm):
    password = forms.CharField(
        label='密码',
        min_length=3,
        max_length=64,
        error_messages={
            'min_length': "密码长度不能小于3个字符",
            'max_length': "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='重复密码',
        min_length=3,
        max_length=64,
        error_messages={
            'min_length': "重复密码长度不能小于3个字符",
            'max_length': "重复密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput())

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'confirm_password', 'email', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] ="form-control"
            field.widget.attrs['placeholder'] = "请输入%s" % (field.label)
            if name in ['password','confirm_password']:
                field.widget.attrs['autocomplete'] ="off"
    def clean_username(self):
        username = self.cleaned_data['username']
        exist = UserInfo.objects.filter(username=username).exists()
        if exist:
            raise ValidationError('用户名已存在')
        return username

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        return encrypt.md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')

        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])

        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')

        return confirm_pwd

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_code(self):
        code = self.cleaned_data['code']
        email = self.cleaned_data.get('email')
        if not email:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(email)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code


class SendEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


    def clean_email(self):
        """ 邮箱校验的钩子 """
        email = self.cleaned_data['email']

        # 判断短信模板是否有问题
        template_id = self.request.GET.get('tpl')
        if not template_id:
            # self.add_error('mobile_phone','短信模板错误')
            raise ValidationError('邮箱模板错误')

        exists = UserInfo.objects.filter(email=email).exists()
        if template_id == 'login':
            if not exists:
                raise ValidationError('邮箱不存在')
        else:
            # 校验数据库中是否已有手机号
            if exists:
                raise ValidationError('邮箱已存在')

        code = random.randrange(1000, 9999)
        # 发送邮件
        sms = send_email_single(email, template_id, code)
        print('ooooooooooooooooooook',sms)
        if sms!=1:
            raise ValidationError("验证码发送失败，{}".format(sms['errmsg']))

        # 验证码 写入redis（django-redis）
        conn = get_redis_connection()
        conn.set(email, code, ex=60)

        return email


class LoginEmailForm(BootStrapForm,forms.Form):
    email = forms.EmailField(label='邮箱',
       )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = UserInfo.objects.filter(email=email).exists()

        if not exists:
            raise ValidationError('邮箱不存在')

        return email

    def clean_code(self):
        code = self.cleaned_data['code']
        email = self.cleaned_data.get('email')

        # 邮箱不存在，则验证码无需再校验
        if not email:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(email)  # 根据邮箱去获取验证码
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code


class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='邮箱或账号')
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True))
    code = forms.CharField(label='图片验证码',widget=forms.TextInput(attrs={'autocomplete':'off'}))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        return encrypt.md5(pwd)

    def clean_code(self):
        """ 钩子 图片验证码是否正确？ """
        # 读取用户输入的yanzhengm
        code = self.cleaned_data['code']

        # 去session获取自己的验证码
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')

        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入错误')

        return code
