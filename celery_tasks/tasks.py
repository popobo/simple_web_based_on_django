# 使用celery
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
import time

# 在任务处理者一端加这几句
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FifthDemo.settings")

application = get_wsgi_application()

# 创建一个Celery类的实例对象
app = Celery("celery_tasks.tasks", broker="redis://127.0.0.1:6379/8")


@app.task
def send_register_active_email(email, username, token):
    subject = "天天习题欢迎你"
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [email]
    html_message = '<h1>%s,欢迎您成为天天习题的注册会员</h1>点击以下链接激活您的账户<br/>' \
                   '<a href="http:///121.192.164.197:8888/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
                       username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)
