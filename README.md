# 食用指南
## 基于django的小说网站

### Django + Scrapy

### 实现功能：
1. 邮箱认证注册，邮箱/用户名登录
2. 小说分类，排行，收藏等功能
3. 小说/作者详情页展示
4. 多级评论，富文本编辑器
5. 用户详细信息登记
6. 书架

#### 数据来源：起点中文网



**必要配置(相关库按照标红自行安装即可)**
新建local_settings.py文件，文件内容如下：
![这是图片](![image](assets/01.jpg)

```python
# -*- coding:utf-8 -*-

LANGUAGE_CODE = 'zh-hans'
#redis 
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 1000,"encoding":"utf-8"},
            "PASSWORD": "***",#密码
        }
    }
}
#mysql
DATABASES = {
#配置数据库链接属性
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
        'NAME': '***',#数据库名
        'USER': '***',#用户名
        'PASSWORD': '***',#密码
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


#邮件相关配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'# 发送邮件配置
EMAIL_HOST = 'smtp.qq.com'# 服务器名称
EMAIL_PORT = 25# 服务端口
EMAIL_HOST_USER = '1454335861@qq.com' # 填写自己邮箱
EMAIL_HOST_PASSWORD = 'hxyzodsziwgzhfaj'# 在邮箱中设置的客户端授权密码
EMAIL_FROM = '罗**'# 收件人看到的发件人
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = True   #是否使用TLS安全传输协议
# EMAIL_USE_SSL = True    #是否使用SSL加密，qq企业邮箱要求使用

```




#### 爬虫使用方法
#### 打开终端
**使用前先注释 return localbook() 语句，运行一次过后再取消注释执行即可**
```
执行下列语句
(爬虫) PS C:\Users\l1\Desktop\scrapy_django> cd qidianspider 
(爬虫) PS C:\Users\l1\Desktop\scrapy_django\qidianspider> cd qidianspider     
(爬虫) PS C:\Users\l1\Desktop\scrapy_django\qidianspider\qidianspider> cd spiders
(爬虫) PS C:\Users\l1\Desktop\scrapy_django\qidianspider\qidianspider\spiders> scrapy crawl thebook
```















