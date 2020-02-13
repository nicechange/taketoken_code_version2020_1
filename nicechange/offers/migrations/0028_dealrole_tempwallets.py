# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-14 14:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('privatemessages', '0009_auto_20180214_1750'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offers', '0027_auto_20180205_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='', max_length=500)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='privatemessages.Thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='offers.Wallet')),
            ],
        ),
        migrations.CreateModel(
            name='TempWallets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_key', models.CharField(max_length=300, verbose_name='Секретный ключ')),
                ('public_key', models.CharField(max_length=300, verbose_name='Публичный ключ')),
                ('btcaddress', models.CharField(max_length=300, verbose_name='Адрес кошелька Bitcoin')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='privatemessages.Thread')),
            ],
        ),
    ]
