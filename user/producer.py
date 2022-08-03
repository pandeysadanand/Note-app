import json

import pika


class RabbitServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    def send_message(self, data):
        channel = self.connection.channel()
        channel.queue_declare(queue='user_signup')
        channel.basic_publish(exchange='',
                              routing_key='user_signup',
                              body=json.dumps(data))

        # print(f" [x] sent {data.get('payload')[1]}")
        self.connection.close()

