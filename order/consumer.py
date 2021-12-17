import json
import os

import django
import pika

# 이 부분은 models를 import 하기전에 해줘야함.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "order.settings")
django.setup()

from user_order.models import Order, Shop

params = pika.URLParameters(
    "amqps://kuwucegv:uH5xcmEg38hdifpeGfSRHsGoA82rA4gd@dingo.rmq.cloudamqp.com/kuwucegv"
)

# RabbitMQ로 connection 만들고
connection = pika.BlockingConnection(params)

# 채널 만들고
channel = connection.channel()

# 해당 consumer가 소비하고 싶은 queue를 declare 함. 즉, order라는 queue의 메시지를 받겠다는 뜻.
channel.queue_declare(queue="order")


def callback(ch, method, properties, body):
    print("Received in order")
    id = json.loads(body)
    print(id)
    order = Order.objects.get(id=id)
    order.deliver_finish = 1
    order.save()

    print("order deliver finished")


channel.basic_consume(queue="order", on_message_callback=callback, auto_ack=True)

print("Started consuming")

channel.start_consuming()

channel.close()
