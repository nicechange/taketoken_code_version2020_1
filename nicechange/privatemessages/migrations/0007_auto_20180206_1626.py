# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-06 13:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('privatemessages', '0006_auto_20180206_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealrole',
            name='wallet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='offers.Wallet'),
        ),
    ]
