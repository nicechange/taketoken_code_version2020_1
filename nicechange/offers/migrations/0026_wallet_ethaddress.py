# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-23 12:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0025_auto_20171225_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='ethaddress',
            field=models.CharField(default='', max_length=300, verbose_name='Адрес кошелька Etherium'),
        ),
    ]
