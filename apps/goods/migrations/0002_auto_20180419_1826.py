# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodscategory',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='goodscategory',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
        migrations.AlterField(
            model_name='goodsimage',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='goodsimage',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
        migrations.AlterField(
            model_name='goodsspu',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='goodsspu',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
        migrations.AlterField(
            model_name='indexcategorygoods',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='indexcategorygoods',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
        migrations.AlterField(
            model_name='indexpromotion',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='indexpromotion',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
        migrations.AlterField(
            model_name='indexslidegoods',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='indexslidegoods',
            name='update_date',
            field=models.DateTimeField(verbose_name='修改时间', auto_now=True),
        ),
    ]
