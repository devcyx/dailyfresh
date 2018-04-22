# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ordergoods',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
    ]
