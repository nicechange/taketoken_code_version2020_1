# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0014_auto_20171026_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='quantity',
            field=models.FloatField(null=True, verbose_name='Цена (руб)'),
        ),
    ]
