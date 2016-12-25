#!/usr/bin/env python
# -*-coding:UTF-8-*-
import pika


class RabbitMQ(object):

    def __init__(self, host, username, password, queue_name, port=5672):
        self.host = host
        self.username = username
        self.password = password
        self.queue_name = queue_name
        self.port = port

    def connect(self):
        # 连接 rabbitmq 服务器
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            self.conn = pika.BlockingConnection(pika.ConnectionParameters(
                self.host, self.port, '/', credentials))
            self.channel = self.conn.channel()
            # 定义队列
            self.channel.queue_declare(queue='queue')
        except Exception, e:
            print e

    def register(self, handle):
        self.handle = handle

    def unregister(self):
        self.handle = None

    def run(self):
        if not hasattr(self, 'conn'):
            self.connect()

        if not hasattr(self, 'callback') and self.callback is not None:
            raise AttributeError('not found callback')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback, queue=self.queue_name)
        self.channel.start_consuming()

    # 定义接收到消息的处理方法
    def callback(self, ch, method, props, body):
        result = self.handle(body)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=str(result))

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body='LUVORC0=')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()
        del self.conn
