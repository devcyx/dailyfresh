from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.core.cache import cache

from apps.goods.models import *
from celery_tasks.tasks import generate_static_index_html


class BaseAdmin(ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 异步生成静态页面
        generate_static_index_html.delay()
        # 清除缓存 防止页面没有更新
        cache.delete('index_data')

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # 异步生成静态页面
        generate_static_index_html.delay()
        # 清除缓存 防止页面没有更新
        cache.delete('index_data')


class GoodsSPUAdmin(BaseAdmin):
    pass


class GoodsSPUAdmin(BaseAdmin):
    pass


class GoodsSKUAdmin(BaseAdmin):
    pass


class GoodsCategoryAdmin(BaseAdmin):
    pass


class IndexSlideGoodsAdmin(BaseAdmin):
    pass


class IndexPromotionAdmin(BaseAdmin):
    pass


admin.site.register(GoodsSPU, GoodsSPUAdmin)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(GoodsCategory, GoodsCategoryAdmin)
admin.site.register(IndexSlideGoods, IndexSlideGoodsAdmin)
admin.site.register(IndexPromotion, IndexPromotionAdmin)
