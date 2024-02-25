import pika

class RabbitMQ():
    def __init__(self,email):
        # 1、连接rabbitmq服务器
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # 2、创建一个名为hello的队列
        channel.queue_declare(queue='sendemail')
        # 3、简单模式,向名为hello队列中插入用户邮箱地址email
        channel.basic_publish(exchange='',
                              routing_key='sendemail',
                              body=email
                              )


        print("发送用户邮箱：‘{}’ 到MQ成功".format(email))
        connection.close()
