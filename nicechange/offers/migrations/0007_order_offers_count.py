# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0006_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='offers_count',
            field=models.IntegerField(default=0, max_length=30),
        ),
    ]
