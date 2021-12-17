import json

import pika

from main import Order, Shop, db

params = pika.URLParameters(
    "amqps://kuwucegv:uH5xcmEg38hdifpeGfSRHsGoA82rA4gd@dingo.rmq.cloudamqp.com/kuwucegv"
)

# RabbitMQ로 connection 만들고
connection = pika.BlockingConnection(params)

# 채널 만들고
channel = connection.channel()

# 해당 consumer가 소비하고 싶은 queue를 declare 함. 즉, order라는 queue의 메시지를 받겠다는 뜻.
channel.queue_declare(queue="boss")


def callback(ch, method, properties, body):
    print("Received in boss")
    data = json.loads(body)
    print(data)

    if properties.content_type == "shop_created":
        shop = Shop(
            id=data["id"],
            shop_name=data["shop_name"],
            shop_address=data["shop_address"],
        )
        db.session.add(shop)
        db.session.commit()

    elif properties.content_type == "shop_updated":
        shop = Shop.query.get(data["id"])
        shop.shop_name = data["shop_name"]
        shop.shop_address = data["shop_address"]
        db.session.commit()

    elif properties.content_type == "shop_deleted":
        shop = Shop.query.get(data)
        db.session.delete(shop)
        db.session.commit()

    elif properties.content_type == "order_created":
        order = Order(id=data["id"], shop=data["shop"], address=data["address"])
        db.session.add(order)
        db.session.commit()

    elif properties.content_type == "order_updated":
        order = Order.query.get(data["id"])
        order.shop = data["shop"]
        order.address = data["address"]
        db.session.commit()

    elif properties.content_type == "order_deleted":
        order = Order.query.get(data)
        db.session.delete(order)
        db.session.commit()


channel.basic_consume(queue="boss", on_message_callback=callback, auto_ack=True)

print("Started consuming")

channel.start_consuming()

channel.close()
