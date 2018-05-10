from threading import Thread
from flask import render_template
from flask_mail import Message
from flask_babel import _
from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# PA does not support multi-thread
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # send_async_email(app, msg)
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_copy_email(user, post, author, time):
    send_email(_('[Microblog] Your copy of post'),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/send_copy.txt',
                                         user=user, post=post, author=author, time=time),
               html_body=render_template('email/send_copy.html',
                                         user=user, post=post, author=author, time=time))
