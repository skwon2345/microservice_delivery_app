import json

import pika

params = pika.URLParameters(
    "amqps://kuwucegv:uH5xcmEg38hdifpeGfSRHsGoA82rA4gd@dingo.rmq.cloudamqp.com/kuwucegv"
)

# RabbitMQ로 connection 만들고
connection = pika.BlockingConnection(params)

# 채널 만들고
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="", routing_key="boss", body=json.dumps(body), properties=properties
    )  # routing_key가 가르키고 있는 곳으로 body의 메시지를 전달하고 싶다는 뜻.
