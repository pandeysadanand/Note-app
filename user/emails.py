from django.conf import settings
from django.core.mail import send_mail


class Email:

    @staticmethod
    def verify_user_email(token, email_id):
        url = "http://127.0.0.1:8000/user/validate/" + token
        msg = f'click on link to verify user. \n{url}'
        # send_mail(subject, message, from_email, [to_email], fail_silently=False)
        send_mail("welcome to note app", msg, settings.EMAIL_HOST_USER, [email_id], fail_silently=False)

    # @staticmethod
    # def verify_user_email(data):
    #     token = EncodeDecode().encode_token(payload=data['id'])
    #     url = "http://127.0.0.1:8000/user/validate/" + token
    #     send_mail("register", url, "testingapis0275@gmail.com", data['email'], fail_silently=False)
