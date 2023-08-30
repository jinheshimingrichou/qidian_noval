from django import template
register = template.Library()
from django.urls import reverse
from web import models
@register.filter(name='limit_brief') # 自定义过滤器
def limit(x,y): # 接受两个值
    if len(x)>y:
        return x[:y]+'...'
    else:
        return x

@register.filter(name='state') # 自定义过滤器
def state(x): # 接受两个值
    if x:
        return '完本'
    else:
        return '连载'


@register.filter(name='prop')  # 自定义过滤器
def prop(x):  # 接受两个值
    if x==1:
        return '免费'
    else:
        return 'VIP'

@register.filter(name='iscollection')  # 自定义过滤器
def iscollection(x,y,z):  # 接受两个值
    return x.filter(book=y,user=z).collection

@register.filter(name='level')  # 自定义过滤器
def level(x):  # 接受两个值
    if x[4:6] in ['白金','大神']:
        return x[4:6]
    else:
        return 'LV???'


import re
@register.filter(name='replace')  # 自定义过滤器
def replace(line):  # 接受两个值r''

    line_split = re.split('(\W+)', line.strip())
    line_split = [line.strip() for line in line_split ]
    return line_split

@register.inclusion_tag('inclusion/menu_list.html')
def manage_menu_list(request):
    data_list = [
        {'title': '人气排行', 'url': reverse("popularity")},
        {'title': '总收藏', 'url': reverse("collection")},
        {'title': '总字数', 'url': reverse("word")},
    ]

    for item in data_list:
        # 当前用户访问的URL：request.path_info:
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'

    return {'data_list': data_list}

@register.inclusion_tag('inclusion/menu_list.html')
def index_nav(request):
    data_list = [
        {'title': '全部', 'url': reverse("index")},
        {'title': '排行', 'url': reverse('rank')},
        {'title': '完本', 'url': reverse("end")},
        {'title': '免费', 'url': reverse("free")},
    ]
    for item in data_list:
        # 当前用户访问的URL：request.path_info:
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'
    return {'data_list': data_list}


@register.inclusion_tag('inclusion/menu_list.html')
def person_nav(request):
    data_list = [
        {'title': '我的首页', 'url': reverse("firstpage")},
        {'title': '我的书架', 'url': reverse("bookshelf")},
        {'title': '消息中心', 'url': reverse("notice:message")},
    ]
    for item in data_list:
        # 当前用户访问的URL：request.path_info:
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'
    return {'data_list': data_list}