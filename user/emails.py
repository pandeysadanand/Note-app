from django.core.mail import send_mail


class Email:

    # @staticmethod
    # def verify_user_email(token, email):
    #     msg = EmailMessage()
    #     msg.set_content(token)
    #
    #     url = "http://127.0.0.1:8000/user/validate/" + token
    #     msg['Subject'] = f'The contents of \n{url}'
    #     msg['From'] = "testingapis0275@gmail.com"
    #     msg['To'] = email
    #
    #     s = smtplib.SMTP('localhost')
    #     s.send_message(msg)
    #     s.quit()

    @staticmethod
    def verify_user_email(token, email):
        url = "http://127.0.0.1:8000/user/validate/" + token
        msg = f'click on link to verify user. \n{url}'
        # send_mail(subject, message, from_email, [to_email], fail_silently=False)
        send_mail("welcome to note app", msg, "testingapis0275@gmail.com", [email], fail_silently=False)
