# -*-coding:UTF-8-*-
import uuid
import pika


class Client(object):

    def __init__(self, host, username, password, queue_name, port=5672):
        credentials = pika.PlainCredentials(username, password)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(
            host, port, '/', credentials))

        self.channel = self.conn.channel()

        # 定义接收返回消息的队列
        self.callback_queue = self.channel.queue_declare(
            exclusive=True).method.queue

        self.channel.basic_consume(self.on_response,
                                   no_ack=True,
                                   queue=self.callback_queue)

    # 定义接收到返回消息的处理方法
    def on_response(self, ch, method, props, body):
        self.result += body
        self.response = body

    def request(self, msg):
        self.result = ''
        self.response = ''
        # 发送请求，并声明返回队列
        self.channel.basic_publish(exchange='',
                                   routing_key='queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=str(uuid.uuid4())
                                   ),
                                   body=msg)
        # 接收返回的数据
        while self.response != 'LUVORC0=':
            self.conn.process_data_events()
        return self.result
