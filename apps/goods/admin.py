from django.contrib import admin

from apps.goods import models

admin.site.register(models.GoodsSPU)
admin.site.register(models.GoodsSKU)
admin.site.register(models.GoodsCategory)