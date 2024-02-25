# base.py文件用于导入django环境，离线脚本初始化用户数据的时候就需要导入django环境
import base
import pika
import time
from django.core.mail import send_mail
from scrapy_django.settings import *

# 1、连接rabbitmq服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host='x.x.x.x'))
channel = connection.channel()
# 2、创建队列,可以只让一方创建，主要是分不清哪边先跑起来，所以这儿也要创建同样的队列
channel.queue_declare(queue='hello')


# 3、构建回调函数
def callback(ch, method, properties, email):
    print("消费者端收到用户邮箱  ‘{}’  成功".format(email))

    subject = '终点中文网'
    if template_id == 'login':
        message = "您的登录验证码是【" + str(template_param_list) + "】，10分钟内有效，请尽快填写"
    else:
        message = "您的注册验证码是【" + str(template_param_list) + "】，10分钟内有效，请尽快填写"
    sender = EMAIL_FROM
    receiver = [email]
    # 讲道理还应该来一个html_message，内容为一个激活链接的a标签
    # send_mail是django内置的发邮件函数，这四个是必须参数
    send_mail(subject, message, sender, receiver)
    time.sleep(5)
    print('向目的邮箱{}发送邮件成功'.format(email))

    # 发送应答信号，表明数据已经处理完成，可以删除,和auto_ack=False套起来用
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 确定监听队列：hello，一旦有值出现，则触发回调函数：callback
channel.basic_consume(queue='hello',
                      auto_ack=False,
                      on_message_callback=callback,
                      )

print('当前MQ简单模式正在等待生产者往消息队列塞消息.......要退出请按 CTRL+C.......')
channel.start_consuming()
