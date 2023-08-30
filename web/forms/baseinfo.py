from django import forms
from web.models import *
from utils import encrypt
from web.forms.bootstrap import BootStrapForm
from django_redis import get_redis_connection
from django.core.exceptions import ValidationError
from utils.tencent.sms import send_email_single
import random
from web.models import UserInfo,BaseInfo

class BaseInfoModelForm(forms.ModelForm):
    introduction = forms.CharField(
        label='简介',
        widget=forms.Textarea())
    sex_choice = (
        (1, '男'),
        (2, '女')
    )
    sex = forms.ChoiceField(label='性别', widget=forms.RadioSelect(), choices=sex_choice)
    class Meta:
        model = BaseInfo
        fields = ['icon','sex','gory','introduction']



