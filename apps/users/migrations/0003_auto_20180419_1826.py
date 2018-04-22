# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
    ]
