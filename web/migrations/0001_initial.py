# Generated by Django 4.2 on 2023-08-26 15:17

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='笔名')),
                ('icon', models.CharField(max_length=255, verbose_name='头像')),
                ('introduction', models.CharField(default='新人', max_length=255, verbose_name='简介')),
                ('book_total', models.IntegerField(default=0, verbose_name='作品数')),
                ('all_word', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='总字数(万)')),
                ('start_work', models.IntegerField(default=0, verbose_name='创作天数')),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='书名')),
                ('book_icon', models.CharField(max_length=255, verbose_name='封面')),
                ('state', models.BooleanField(default=False, verbose_name='状态')),
                ('prop', models.SmallIntegerField(choices=[(1, '免费'), (2, 'VIP')], verbose_name='属性')),
                ('type', models.CharField(max_length=10, verbose_name='书的种类大')),
                ('category', models.CharField(max_length=30, verbose_name='书的类型小')),
                ('word', models.CharField(max_length=30, verbose_name='字数')),
                ('brief', models.TextField(default='这个人很懒，还没有写简介', verbose_name='简介')),
                ('collection', models.BooleanField(default=False, verbose_name='收藏')),
                ('recommend', models.BigIntegerField(verbose_name='推荐票')),
                ('author', models.ForeignKey(db_column='author', on_delete=django.db.models.deletion.CASCADE, to='web.authors', verbose_name='作者')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=30, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('email', models.EmailField(max_length=30, verbose_name='邮箱')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='内容')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('book', models.ForeignKey(db_column='book', on_delete=django.db.models.deletion.DO_NOTHING, to='web.books', verbose_name='评论作品')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='web.comment')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replyers', to='web.userinfo')),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to='web.userinfo', verbose_name='评论者')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Collections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coll_num', models.PositiveIntegerField(blank=0, verbose_name='收藏数')),
                ('bookname', models.ForeignKey(db_column='bookname', on_delete=django.db.models.deletion.CASCADE, to='web.books', verbose_name='书名')),
            ],
        ),
        migrations.CreateModel(
            name='BaseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(blank=True, upload_to='user/', verbose_name='头像')),
                ('introduction', models.CharField(default='暂无相关介绍', max_length=255, verbose_name='简介')),
                ('sex', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别')),
                ('gory', models.CharField(max_length=10, verbose_name='地区')),
                ('level', models.SmallIntegerField(choices=[(1, 'LV1'), (2, 'LV2'), (3, 'LV3'), (4, 'LV4'), (5, 'LV5')], default=1, verbose_name='等级')),
                ('dianbi', models.PositiveIntegerField(verbose_name='点币')),
                ('name', models.OneToOneField(db_column='name', on_delete=django.db.models.deletion.CASCADE, to='web.userinfo', verbose_name='用户名')),
            ],
        ),
    ]
