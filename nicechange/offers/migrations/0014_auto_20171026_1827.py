# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0013_auto_20171019_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='demand_type',
        ),
        migrations.AlterField(
            model_name='offer',
            name='quantity',
            field=models.FloatField(null=True, verbose_name='Предлагаемая цена покупки/продажи'),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.FloatField(null=True, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='quantity',
            field=models.FloatField(null=True, verbose_name='Количество'),
        ),
    ]
