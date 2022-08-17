from . import create_app, mail
from flask_mail import Message
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


def send_mail(subject: str, body: str, to: str):
    msg = Message(subject,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = body
    return mail.send(msg)
