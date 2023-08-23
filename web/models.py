from django.db import models


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
    collection = models.BooleanField(verbose_name='收藏', default=False)
    recommend = models.BigIntegerField(verbose_name='推荐票')


class MonthTicks(models.Model):
    tick_seq=models.CharField(verbose_name='票号',max_length=30, unique=True)
    votework=models.ForeignKey(verbose_name='投票作品',to='Books',db_column='votework',on_delete=models.DO_NOTHING)
    voteuser=models.ForeignKey(verbose_name='投票人',to='UserInfo',db_column='voteuser',on_delete=models.DO_NOTHING)
    datetime=models.DateTimeField(verbose_name='投票日期')


class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=30, db_index=True)  # ID
    password = models.CharField(verbose_name="密码", max_length=32)  # 密码
    email = models.EmailField(verbose_name="邮箱", max_length=30)
