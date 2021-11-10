from django.core.mail import EmailMessage
import threading
from datetime import datetime
from django.conf import settings

class EmailThread(threading.Thread):

    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()




class SendEmail:

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject =data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        EmailThread(email).start()
        

# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return f'{phone}{datetime.date(datetime.now())}{settings.SECRET_KEY}'