# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-20 14:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offers', '0016_auto_20171120_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('burse', models.CharField(choices=[('Pocket-Exchange', 'Pocket-Exchange'), ('КэшБанк', 'КэшБанк'), ('Bitochek', 'Bitochek'), ('SBitcoin', 'SBitcoin'), ('WW-Pay', 'WW-Pay'), ('CashTransfers', 'CashTransfers'), ('NewLine', 'NewLine'), ('PayToChina', 'PayToChina'), ('24PayBank', '24PayBank'), ('60сек', '60сек'), ('ProstoCash', 'ProstoCash'), ('PayGet', 'PayGet'), ('ObmenoFF', 'ObmenoFF'), ('YChanger', 'YChanger'), ('BetaTransfer', 'BetaTransfer'), ('CoinToCard', 'CoinToCard'), ('100Btc', '100Btc'), ('Банкомат', 'Банкомат'), ('E-Obmen', 'E-Obmen'), ('JoJoCash', 'JoJoCash'), ('Buy-Bitcoins', 'Buy-Bitcoins'), ('BaksMan', 'BaksMan'), ('FastChange', 'FastChange'), ('X-Pay', 'X-Pay'), ('MinedTrade', 'MinedTrade'), ('GoldObmen', 'GoldObmen'), ('BitPayeers', 'BitPayeers'), ('CryptoMoney', 'CryptoMoney'), ('BitExchanger', 'BitExchanger'), ('Касса', 'Касса'), ('Pay-Today', 'Pay-Today'), ('PM-Obmen', 'PM-Obmen'), ('BTC2Cashin', 'BTC2Cashin'), ('Bit-Обменка', 'Bit-Обменка'), ('WuBill', 'WuBill'), ('MagneticExchange', 'MagneticExchange')], max_length=30, verbose_name='Биржа')),
                ('type_of_token', models.CharField(choices=[('BTC', 'BTC'), ('LTC', 'LTC'), ('ETH', 'ETH'), ('DASH', 'DASH'), ('ZEC', 'ZEC'), ('XMR', 'XMR')], default='BTC', max_length=30, verbose_name='Тип валюты')),
                ('sellorbuy', models.CharField(choices=[('ПРОДАЖА', 'ПРОДАЖА'), ('ПОКУПКА', 'ПОКУПКА')], default='ПРОДАЖА', max_length=30, null=True, verbose_name='Продать/купить')),
                ('percent', models.FloatField(null=True, verbose_name='Процент от курса')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
