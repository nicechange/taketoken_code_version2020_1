# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-06 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0021_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='address',
            field=models.CharField(max_length=300, verbose_name='Адрес кошелька Bitcoin'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.CharField(default='0', max_length=300, verbose_name='Баланс'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='private_key',
            field=models.CharField(max_length=300, verbose_name='Секретный ключ'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='public_key',
            field=models.CharField(max_length=300, verbose_name='Публичный ключ'),
        ),
    ]
