from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer

from dailyfresh import settings
from utils.models import BaseModel


class User(BaseModel, AbstractUser):
    """用户模型类"""

    def generate_active_token(self):
        """生成激活令牌"""
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        token = serializer.dumps({"confirm": self.id})  # type:bytes
        return token.decode()

    class Meta(object):
        db_table = 'df_user'


class Address(BaseModel):
    """用户地址"""

    receiver_name = models.CharField(max_length=20, verbose_name='收件人')
    receiver_mobile = models.CharField(max_length=11, verbose_name='联系电话')
    detail_addr = models.CharField(max_length=256, verbose_name='详细地址')
    zip_default = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    user = models.ForeignKey(User, verbose_name='所属用户')

    class Meta(object):
        db_table = 'df_address'
