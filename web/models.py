from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.urls import reverse
# Create your models here.

class Authors(models.Model):
    name = models.CharField(verbose_name='笔名',max_length=30, unique=True)  #
    icon = models.CharField(verbose_name='头像',max_length=255)  #
    introduction = models.CharField(verbose_name='简介',max_length=255, default="新人")  #
    book_total = models.IntegerField(verbose_name='作品数',default=0)  #
    all_word = models.DecimalField(verbose_name='总字数(万)',max_digits=7, decimal_places=2)  #
    start_work = models.IntegerField(verbose_name='创作天数',default=0)  #


# class Categorys(models.Model):
#     type = models.CharField(verbose_name='书的类大',max_length=10)  #
#     category = models.CharField(verbose_name='书的类型小',max_length=30)  #

class Collections(models.Model):
    bookname=models.ForeignKey(verbose_name='书名',to='Books',db_column='bookname',on_delete=models.CASCADE)
    coll_num=models.PositiveIntegerField(verbose_name='收藏数',blank=0)

class Books(models.Model):
    name = models.CharField(verbose_name='书名',max_length=30, unique=True)  #
    author = models.ForeignKey(verbose_name='作者',to='Authors',db_column='author', on_delete=models.CASCADE, )  #
    book_icon = models.CharField(verbose_name='封面',max_length=255)  #
    state = models.BooleanField(verbose_name='状态',default=False)  #flase连载，true完结
    prop_choice = (
        (1, '免费'),
        (2, 'VIP')
    )
    prop=models.SmallIntegerField(verbose_name='属性', choices=prop_choice)
    type = models.CharField(verbose_name='书的种类大', max_length=10)
    category = models.CharField(verbose_name='书的类型小', max_length=30)
    word=models.CharField(verbose_name='字数',max_length=30)
    brief = models.TextField(verbose_name='简介', default='这个人很懒，还没有写简介')
    recommend = models.BigIntegerField(verbose_name='推荐票')

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id])

class MyViewBook(models.Model):
    #我的书架
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', db_column='user', on_delete=models.CASCADE)
    book = models.ForeignKey(verbose_name='收藏作品', to='Books', db_column='book', on_delete=models.CASCADE)
    collection = models.BooleanField(verbose_name='收藏', default=False)
    time = models.DateTimeField(verbose_name='阅读时间', auto_now_add=True)  # 收藏时间

# class Poll(models.Model):
#     # 投票记录
#     votework=models.ForeignKey(verbose_name='投票作品',to='Books',db_column='votework',on_delete=models.DO_NOTHING)
#     voteuser=models.ForeignKey(verbose_name='投票人',to='UserInfo',db_column='voteuser',on_delete=models.DO_NOTHING)
#     datetime=models.DateTimeField(verbose_name='投票日期')
#     tick_choice = (
#         (1, '推荐票'),
#         (2, '月票')
#     )
#     tick= models.SmallIntegerField(verbose_name='属性', choices=tick_choice)
#


class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=30, db_index=True)  # ID
    password = models.CharField(verbose_name="密码", max_length=32)  # 密码
    email = models.EmailField(verbose_name="邮箱", max_length=30)

class BaseInfo(models.Model):
    # 个人基本信息
    name = models.OneToOneField(verbose_name='用户名', to='UserInfo',db_column='name',on_delete=models.CASCADE)  #
    icon = models.ImageField(verbose_name='头像',upload_to='user/', blank=True) #
    introduction = models.CharField(verbose_name='简介', max_length=255, default="暂无相关介绍")  #
    sex_choice = (
        (1, '男'),
        (2, '女')
    )
    sex = models.SmallIntegerField(verbose_name='性别', choices=sex_choice,default=1)
    gory=models.CharField(verbose_name='地区',max_length=10,)
    level_choice = (
        (1, 'LV1'),
        (2, 'LV2'),
        (3, 'LV3'),
        (4, 'LV4'),
        (5, 'LV5'),

    )
    level = models.SmallIntegerField(verbose_name='等级', choices=level_choice,default=1)
    dianbi=models.PositiveIntegerField(verbose_name='点币')


# class BillFold(models.Model):
#     # 票夹
#     name = models.ForeignKey(verbose_name='用户名', to='UserInfo',db_column='name',on_delete=models.CASCADE)  #
#     recom=models.PositiveIntegerField(verbose_name='推荐票数')
#     month = models.PositiveIntegerField(verbose_name='月票数')

# class Recharge(models.Model):
#     # 充值记录
#     name = models.ForeignKey(verbose_name='用户名', to='UserInfo', db_column='name', on_delete=models.CASCADE)
#     order = models.CharField(verbose_name='订单号', max_length=64, unique=True)  # 唯一索引
#     count = models.IntegerField(verbose_name='充值金额')
#     price = models.IntegerField(verbose_name='实际支付价格')
#     create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# django-mptt
from mptt.models import MPTTModel, TreeForeignKey
class Comment(MPTTModel):
    #评论
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', db_column='user', on_delete=models.CASCADE)
    book = models.ForeignKey(verbose_name='评论作品', to='Books', db_column='book', on_delete=models.DO_NOTHING)

    content= RichTextUploadingField(verbose_name='内容')
    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(UserInfo, null=True, blank=True, on_delete=models.CASCADE, related_name='replyers')
    class MPTTMeta:
        order_insertion_by = ['created']

    def get_user(self):
        return self.user

