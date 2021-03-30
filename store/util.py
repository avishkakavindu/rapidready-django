import threading
from decouple import config
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        msg_plain = render_to_string('email/email_normal_email.txt', data['email_body'])
        msg_html = render_to_string('email/email_normal_email.html', data['email_body'])

        msg = EmailMultiAlternatives(data['email_subject'], msg_plain, config('EMAIL_HOST_USER'), [data['receiver']])
        msg.attach_alternative(msg_html, "text/html")

        EmailThread(msg).start()