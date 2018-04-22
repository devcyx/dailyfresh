from __future__ import absolute_import
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')


from celery import Celery
from django.core.mail import send_mail

from dailyfresh import settings

app = Celery('celery_task.tasks', broker='redis://127.0.0.1:6379/1')


@app.task
def send_active_mail(username, receiver, token):
    """封装发送邮件的方法"""
    subject = '天天生鲜激活邮件'  # 邮件标题
    message = ''  # 邮件正文
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [receiver]  # 收件人 列表
    html_message = ('<h2>尊敬的 %s, 感谢注册天天生鲜</h2>'
                    '<p>请点击此链接激活您的帐号: '
                    '<a href="http://127.0.0.1:8000/users/active/%s">'
                    'http://127.0.0.1:8000/users/active/%s</a>'
                    ) % (username, token, token)

    # 发送邮件的方法
    send_mail(subject, message, sender, receiver, html_message=html_message)
