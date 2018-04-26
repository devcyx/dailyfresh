from celery.utils.serialization import _datetime_to_json
import json

from django.core.cache import cache
from django.core.paginator import Paginator
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django_redis import get_redis_connection
from redis.client import StrictRedis

from apps.goods.models import GoodsCategory, IndexSlideGoods, IndexPromotion, IndexCategoryGoods, GoodsSKU, GoodsSPU


class CartCountView(View):
    """计算购物车数量类"""

    def c_cart(self, request):
        count = 0
        # 如果是登陆状态
        if request.user.is_authenticated():
            strict_redis = get_redis_connection()  # type:StrictRedis
            keys = 'cart_{}'.format(request.user.id)
            # print(keys)
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
            # cart_json = request.session.get('cart')
            # cart_count = json.loads(cart_json)  # type:dict
            # for value in cart_count.values():
            #     count += int(value)
            pass
        return count


class IndexView(CartCountView):
    def get(self, request):
        # 保存cookie
        # cart_json = json.dumps({'1': '2', '2': '2'})
        # response = HttpResponse('保存cart cookie成功！')
        # response.set_cookie('cart', cart_json, 3600 * 24 * 10)
        # return response

        # 保存session
        # cart_json = json.dumps({'1': '2', '2': '5'})
        # request.session['cart'] = cart_json

        # 取缓存数据
        context = cache.get('index_data')

        if not context:
            # print('没有缓存')
            # 没有缓存 查询mysql数据库数据
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

            # 返回的字典
            context = {
                'categorys': categorys,
                'slides': slides,
                'promotions': promotions,
            }

            # 查询完成 放入redis用于缓存
            cache.set('index_data', context, 60 * 45)
        # else:
        #     print('有缓存！')

        # 显示购物车数量
        cart_count = self.c_cart(request)
        context['cart_count'] = cart_count

        return render(request, 'goods/index.html', context)


class DetailView(CartCountView):
    """商品详情页"""

    def get(self, request, sku_id):
        # 查询数据
        # 商品sku表
        sku = GoodsSKU.objects.get(id=sku_id)
        # 商品类别表
        categorys = GoodsCategory.objects.all()
        # 商品SPU表
        spu = GoodsSPU.objects.get(id=sku.spu.id)

        # 新品推荐数据
        new_skus = GoodsSKU.objects.filter(category=sku.category).order_by('-create_date')[0:2]

        # 其他规格的商品
        other_skus = GoodsSKU.objects.filter(spu=sku.spu.id).exclude(id=sku_id)

        # 购物车
        cart_count = self.c_cart(request)

        context = {
            'sku': sku,
            'categorys': categorys,
            'spu': spu,
            'new_skus': new_skus,
            'cart_count': cart_count,
            'other_skus': other_skus,
        }

        # 如果用户登陆 保存浏览记录
        user = request.user
        if user.is_authenticated():
            strict_redis = get_redis_connection()  # type:StrictRedis
            key = 'history_%s' % user.id
            # 删除相同的浏览记录
            strict_redis.lrem(key, 0, sku_id)
            # 向左边插入浏览记录
            strict_redis.lpush(key, sku_id)
            # 只保存5条记录 取左边开始前5条
            strict_redis.ltrim(key, 0, 4)

        return render(request, 'goods/detail.html', context)


class ListView(CartCountView):
    """全部商品列表页"""

    def get(self, request, category_id, page_number):
        # 商品类别表
        category = GoodsCategory.objects.get(id=category_id)
        categorys = GoodsCategory.objects.all()

        # 商品sku表
        skus = GoodsSKU.objects.filter(category=category.id)

        # 新品推荐数据
        new_skus = GoodsSKU.objects.filter(category=category.id).order_by('-create_date')[0:2]

        # 购物车
        cart_count = self.c_cart(request)

        context = {
            'categorys': categorys,
            'category': category,
            'new_skus': new_skus,
            'cart_count': cart_count,
        }
        # 分页显示
        # 参数一 要分页所有数据
        # 参数二 每页显示的数据
        sku_paginator = Paginator(skus, 5)
        if page_number:
            context['page_data'] = sku_paginator.page(page_number)
            return render(request, 'goods/list.html', context)
        else:
            context['page_data'] = sku_paginator.page(1)
            return render(request, 'goods/list.html', context)
