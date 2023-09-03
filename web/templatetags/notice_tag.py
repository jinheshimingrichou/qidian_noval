from django import template
register = template.Library()
from django.urls import reverse
from web.models import *
@register.filter(name='notice_unread')
def notice_unread(instance):
    count=Messages.objects.filter(receiver=instance).filter(is_read=False).count()
    return count