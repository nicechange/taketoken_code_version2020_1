# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-14 09:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0007_order_offers_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='offers_count',
            field=models.IntegerField(default=0),
        ),
    ]
