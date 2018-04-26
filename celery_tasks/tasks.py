# from __future__ import absolute_import
# import os
# import django
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
# django.setup()
from time import time

from django.template import loader
from apps.goods.models import IndexCategoryGoods, GoodsCategory, IndexSlideGoods, IndexPromotion
from celery import Celery
from django.core.mail import send_mail

from dailyfresh import settings

app = Celery('dailyfresh', broker='redis://127.0.0.1:6379/1')


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


@app.task
def generate_static_index_html():
    """显示首页"""
    # 商品类别表
    time.seelp(2)
    categorys = GoodsCategory.objects.all()
    # 首页轮播图表
    slides = IndexSlideGoods.objects.all().order_by('index')
    # 首页促销活动表
    promotions = IndexPromotion.objects.all().order_by('index')[0:2]

    # 首页分类展示表
    for c_sku in categorys:
        text_skus = IndexCategoryGoods.objects.filter(category=c_sku, display_type=0).order_by('-index')
        pht_skus = IndexCategoryGoods.objects.filter(category=c_sku, display_type=1).order_by('-index')
        # 动态给类增加属性
        c_sku.pht = pht_skus
        c_sku.text = text_skus

    # 返回的字典
    context = {
        'categorys': categorys,
        'slides': slides,
        'promotions': promotions,
    }
    # 获取模板数据
    template = loader.get_template('goods/index.html')
    # 渲染模板
    html_str = template.render(context)

    # 写入数据到静态文件
    with open('/home/python/Desktop/static/index.html', 'w') as f:
        f.write(html_str)
