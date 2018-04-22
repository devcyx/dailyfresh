from django.db import models


class BaseModel(models.Model):
    """模型类的基类"""

    # 创建时间
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', )
    # 修改时间
    update_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta(object):
        abstract = True
