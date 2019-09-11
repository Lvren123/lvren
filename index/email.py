from celery import task
from django.core.mail import EmailMessage
import time

@task
def sendmail(email):
    # esend = EmailMessage('欢迎注册','点击此链接<a href="http://localhost:8000/valid_email?code='+code+'">验证</a>',DEFAULT_FROM_EMAIL,email)
    # esend.content_subtype = 'html'
    # esend.send()
    time.sleep(10)