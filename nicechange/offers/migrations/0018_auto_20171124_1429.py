# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-24 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0017_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='BurseCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('burse', models.CharField(max_length=30, verbose_name='Биржа')),
                ('token', models.CharField(max_length=30, verbose_name='Токен')),
                ('type', models.CharField(max_length=30, verbose_name='Тип операции')),
                ('course', models.FloatField(null=True, verbose_name='Курс')),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='burse',
            field=models.CharField(choices=[('BTC', 'BTC'), ('LTC', 'LTC'), ('ETH', 'ETH')], max_length=30, verbose_name='Биржа'),
        ),
        migrations.AlterField(
            model_name='course',
            name='type_of_token',
            field=models.CharField(choices=[('BTC', 'BTC'), ('LTC', 'LTC'), ('ETH', 'ETH')], default='BTC', max_length=30, verbose_name='Тип валюты'),
        ),
    ]
