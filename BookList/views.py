# from django.shortcuts import render,HttpResponse
# import random
# # Create your views here.
# from django import forms
# from BookList.models import *
# from django.conf import settings

#
# def send_sms(request):
#     """ 发送短信
#         ?tpl=login  -> 548762
#         ?tpl=register -> 548760
#     """
#     tpl = request.GET.get('tpl')
#     template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
#     if not template_id:
#         return HttpResponse('模板不存在')
#
#     code = random.randrange(1000, 9999)
#     res = send_sms_single('15131289', template_id, [code, ])
#     if res['result'] == 0:
#         return HttpResponse('成功')
#     else:
#         return HttpResponse(res['errmsg'])
import redis
from django.shortcuts import render,HttpResponse
from django_redis import get_redis_connection

def index(request):
    conn = get_redis_connection("default")
    conn.set('nickname','lms',ex=10)
    value=conn.get('nickname')
    print(value)
    return HttpResponse('ok')

class RegisterModelFrom(forms.ModelForm):
    password=forms.CharField(label="密码",widget=forms.PasswordInput())
    comfirm_password = forms.CharField(label="重复密码", widget=forms.PasswordInput())
    code=forms.CharField(label="验证码")
    class Meta:
        model=UserInfo
        fields='__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']="form-contorl"
            field.widget.attrs['placeholder'] = "请输入%s"%(field.label)

def Register(request):
    form=RegisterModelFrom()
    return render(request, 'book/register.html', {'form':form})
