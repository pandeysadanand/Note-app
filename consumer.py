import smtplib
import sys
from email.message import EmailMessage

import pika


def verify_user_email(body):
    msg = EmailMessage()
    msg.set_content(body.get("token"))

    url = "http://127.0.0.1:8000/user/validate/" + body.get("token")
    msg['Subject'] = f'The contents of \n{url}'
    msg['From'] = 'testingapis0275@gmail.com'
    msg['To'] = [body.get('email')]

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()


def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='user_signup')

        def callback(ch, method, properties, body):
            verify_user_email(body)
            print(">>>>>>>>>>>>>>>>>")
            print(" [x] Received %r" % body)

        channel.basic_consume(queue='user_signup', on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
    print('Interrupted')
    sys.exit(0)
