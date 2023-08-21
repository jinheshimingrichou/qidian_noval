from django.db import models

# Create your models here.

# class Authors(models.Model):
#     name=models.CharField(max_length=30,unique=True,primary_key=True)#姓名
#     icon=models.CharField(max_length=255)#头像
#     introduction=models.CharField(max_length=30,default="新人")#简介
#     book_total=models.IntegerField(default=0)#作品数
#     all_word=models.DecimalField(max_length=7,decimal_places=2)#总字数
#     start_work=models.IntegerField(default=0)#创作天数
#
# class Books(models.Model):
#     name=models.CharField(max_length=30,unique=True)#书名
#     author=models.ForeignKey(Authors,on_delete=models.CASCADE,)#作者
#     book_icon=models.CharField(max_length=255)#封面
#     state=models.CharField(max_length=10,default="完结")#书的状态
#     category=models.ForeignKey(Categorys,max_length=30)#书的类型小
#     brief=models.CharField(max_length=255,default='这个人很懒，还没有写简介')
#
# class Categorys(models.Model):
#      category= models.CharField(max_length=30)#书的类型小
#      type = models.CharField(max_length=10)  # 书的种类大

# class UserInfo(models.Model):
#     username = models.CharField(verbose_name='用户名',max_length=30)  # ID
#     password=models.CharField(verbose_name="密码",max_length=10)#密码
#

