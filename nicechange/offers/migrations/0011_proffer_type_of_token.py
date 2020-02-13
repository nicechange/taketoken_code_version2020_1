# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0010_auto_20171017_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='proffer',
            name='type_of_token',
            field=models.CharField(choices=[('BTC', 'BTC'), ('LTC', 'LTC'), ('ETH', 'ETH'), ('DASH', 'DASH'), ('ZEC', 'ZEC'), ('XMR', 'XMR')], default='BTC', max_length=30, verbose_name='Тип валюты'),
        ),
    ]
