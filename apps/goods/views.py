from celery.utils.serialization import _datetime_to_json
import json
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django_redis import get_redis_connection
from redis.client import StrictRedis

from apps.goods.models import GoodsCategory, IndexSlideGoods, IndexPromotion, IndexCategoryGoods


class CartCountView(View):
    """计算购物车数量类"""

    def c_cart(self, request):
        count = 0
        # 如果是登陆状态
        if request.user.is_authenticated():
            strict_redis = get_redis_connection()  # type:StrictRedis
            keys = 'cart_{}'.format(request.user.id)
            print(keys)
            for i in strict_redis.hvals(keys):
                count += int(i)
        else:
            # todo:如果是未登录状态
            # 在cookie中取购物车数量
            # cart_json = request.COOKIES.get('cart')
            # cart_count = json.loads(cart_json)  # type:dict
            # for value in cart_count.values():
            #     count += int(value)

            # 从session中取购物车数量
            cart_json = request.session.get('cart')
            cart_count = json.loads(cart_json)  # type:dict
            for value in cart_count.values():
                count += int(value)
        return count


class IndexView(CartCountView):
    def get(self, request):
        # 保存cookie
        # cart_json = json.dumps({'1': '2', '2': '2'})
        # response = HttpResponse('保存cart cookie成功！')
        # response.set_cookie('cart', cart_json, 3600 * 24 * 10)
        # return response

        # 保存session
        cart_json = json.dumps({'1': '2', '2': '5'})
        request.session['cart'] = cart_json
        # 商品类别表
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

        # 显示购物车数量
        count = self.c_cart(request)

        # 返回的字典
        context = {
            'categorys': categorys,
            'slides': slides,
            'promotions': promotions,
            'cart_count': count,
        }
        return render(request, 'goods/index.html', context)
