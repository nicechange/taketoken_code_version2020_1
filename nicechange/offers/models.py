# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from presentation.models import CBit, CEther, CLite
from privatemessages.models import Thread

class Order(models.Model):
    owner = models.CharField(max_length=30, default='User', verbose_name="Владелец")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='Open', verbose_name="Статус")
    SELLORBUY_CHOISES = (
        ('ПРОДАЖА', 'ПРОДАЖА'),
        ('ПОКУПКА', 'ПОКУПКА'),
    )
    sellorbuy = models.CharField(max_length=30, null=True, choices=SELLORBUY_CHOISES,
                                 default='ПРОДАЖА', verbose_name="Продать/купить")
    BANK_CHOISES = (
        ('Сбербанк', 'Сбербанк'),
        ('Альфабанк', 'Альфабанк'),
        ('Тинькофф-банк', 'Тинькофф-банк'),
    )

    quantity = models.FloatField(null=True, blank=True, verbose_name="Количество")

    fiat = models.FloatField(null=True, blank=True, verbose_name="Сумма в фиатной валюте")

    bank = models.CharField(max_length=30, null=True, choices=BANK_CHOISES,
                                 default='Сбербанк', verbose_name="Банк")
    date = models.DateField(default=now, verbose_name='Дата')
    OFFER_TYPE_CHOISES = (
        ('DASH', 'DASH'),
        ('ZEC', 'ZEC'),
        ('XMR', 'XMR'),
        ('BTC', 'BTC'),
        ('LTC', 'LTC'),
        ('ETH', 'ETH'),
    )
    offer_type = models.CharField(max_length=30, null=True, verbose_name="Что продаю/покупаю", choices=OFFER_TYPE_CHOISES,
                                 default='BTC',)
    #demand_type = models.CharField(max_length=30, null=True, verbose_name="Что хочу получить/предложить")
    offers_count = models.IntegerField(default=0, verbose_name="Количество сделок")
    state = models.CharField(max_length=30, default='Draft', verbose_name="Статус")

class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='Sent', verbose_name="Статус")
    date = models.DateField(default=now, verbose_name="Дата")
    quantity = models.FloatField(null=True, verbose_name="Цена")
    information = models.CharField(max_length=30, null=True, verbose_name="Информация")

class Proffer(models.Model):
    TYPE_CHOISES = (
        ('КУПЛЮ', 'КУПЛЮ'),
        ('ПРОДАМ', 'ПРОДАМ'),
    )
    type = models.CharField(max_length=30, choices=TYPE_CHOISES, default='КУПЛЮ',
                                     verbose_name="Тип")
    owner = models.CharField(max_length=30, default='User', verbose_name="Владелец")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='Open', verbose_name="Статус")
    date = models.DateField(default=now, verbose_name="Дата")
    TOKEN_TYPE_CHOISES = (
        ('BTC', 'BTC'),
        ('LTC', 'LTC'),
        ('ETH', 'ETH'),
        ('DASH', 'DASH'),
        ('ZEC', 'ZEC'),
        ('XMR', 'XMR'),
    )
    BANK_CHOISES = (
        ('Сбербанк', 'Сбербанк'),
        ('Тинькофф', 'Тинькофф'),
        ('Втб-24', 'Втб-24'),
        ('Промсвязьбанк', 'Промсвязьбанк'),
        ('Альфабанк', 'Альфабанк'),
        ('Яндекс.Деньги', 'Яндекс.Деньги'),
        ('Qiwi', 'Qiwi'),
    )
    bank_search = models.CharField(max_length=30, choices=BANK_CHOISES, default='Сбербанк',
                                     verbose_name="Способ оплаты")
    bank = models.CharField(max_length=200, default='Сбербанк', verbose_name="Банк")
    bank_sber = models.BooleanField(default=True, verbose_name="Сбербанк")
    bank_tinkoff = models.BooleanField(default=False, verbose_name="Тинькофф")
    bank_vtb = models.BooleanField(default=False, verbose_name="Втб-24")
    bank_promsvyaz = models.BooleanField(default=False, verbose_name="Промсвязьбанк")
    bank_alfa = models.BooleanField(default=False, verbose_name="Альфабанк")
    bank_yandex = models.BooleanField(default=False, verbose_name="Яндекс.Деньги")
    bank_qiwi = models.BooleanField(default=False, verbose_name="Qiwi")
    type_of_token = models.CharField(max_length=30, choices=TOKEN_TYPE_CHOISES, default='BTC', verbose_name="Крипта")
    rate = models.FloatField(max_length=200, default=0, verbose_name="Курс")
    replies_count = models.IntegerField(default=0, verbose_name="Кол-во ответов")
    state = models.CharField(max_length=30, default='Draft', verbose_name="Статус")
    info = models.CharField(max_length=300, default='Нет', verbose_name="Комментарий")
    min = models.FloatField(max_length=200, default=0, verbose_name="Минимальная сумма")
    max = models.FloatField(max_length=200, default=0, verbose_name="Максимальная сумма")
    limit = models.CharField(max_length=200, default='Нет', verbose_name="Лимит")
    balance = models.FloatField(max_length=200, default=0, verbose_name="Баланс")
    brs = models.CharField(max_length=30, null=True, verbose_name="Биржа")
    prc = models.FloatField(null=True, verbose_name="Процент от курса")

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, default=None, related_name='owner', on_delete=models.CASCADE)
    proffer = models.ForeignKey(Proffer, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='Sent', verbose_name="Статус")
    date = models.DateField(default=now, verbose_name="Дата")
    time = models.TimeField(auto_now=True)
    SELLORBUY_CHOISES = (
        ('ПРОДАЖА', 'ПРОДАЖА'),
        ('ПОКУПКА', 'ПОКУПКА'),
    )
    sellorbuy = models.CharField(max_length=30, null=True, choices=SELLORBUY_CHOISES,
                                 default='ПРОДАЖА', verbose_name="Продать/купить")
    quantity = models.FloatField(null=True, verbose_name="Количество")
    thread = models.ForeignKey(Thread, null=True, on_delete=models.CASCADE)
    trying = models.BooleanField(default=False, verbose_name="Попытка подтверждения")
    confirm = models.BooleanField(default=False, verbose_name="Подтверждение")
    bank = models.CharField(max_length=200, default='Нет', verbose_name="Банк")
    price = models.FloatField(max_length=200, default=0, verbose_name="Сумма")

class BurseCourse(models.Model):
    burse = models.CharField(max_length=30, verbose_name="Биржа")
    token = models.CharField(max_length=30, verbose_name="Токен")
    course = models.FloatField(null=True, verbose_name="Курс")

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    BURSE_CHOISES = (
        ('Bittrex', 'Bittrex'),
        ('Bitfinex', 'Bitfinex'),
        ('Poloniex', 'Poloniex'),
        ('Kraken', 'Kraken'),
    )
    burse = models.CharField(max_length=30, choices=BURSE_CHOISES, verbose_name="Биржа")
    TOKEN_TYPE_CHOISES = (
        ('BTC', 'BTC'),
        #('LTC', 'LTC'),
        #('ETH', 'ETH'),
        #('DASH', 'DASH'),
        #('ZEC', 'ZEC'),
        #('XMR', 'XMR'),
    )
    type_of_token = models.CharField(max_length=30, choices=TOKEN_TYPE_CHOISES, default='BTC', verbose_name="Крипта")
    SELLORBUY_CHOISES = (
        ('ПРОДАЖА', 'ПРОДАЖА'),
        ('ПОКУПКА', 'ПОКУПКА'),
    )
    sellorbuy = models.CharField(max_length=30, null=True, choices=SELLORBUY_CHOISES,
                                 default='ПРОДАЖА', verbose_name="Продать/купить")
    percent = models.FloatField(null=True, verbose_name="Процент от курса")


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    private_key = models.CharField(max_length=300, verbose_name="Секретный ключ")
    public_key = models.CharField(max_length=300, verbose_name="Публичный ключ")
    btcaddress = models.CharField(max_length=300, verbose_name="Адрес кошелька Bitcoin")
    ethaddress = models.CharField(max_length=300, default="", verbose_name="Адрес кошелька Etherium")
    btcbalance = models.CharField(max_length=300, default='0.00000000', verbose_name="Баланс BTC")
    ethbalance = models.CharField(max_length=300, default='0.00000000', verbose_name="Баланс ETH")
    trying = models.BooleanField(default=False, verbose_name="Попытка подтверждения")
    confirm = models.BooleanField(default=False, verbose_name="Подтверждение")

class DealRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    role = models.CharField(max_length=500, default='')
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)

class TempWallets(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    private_key = models.CharField(max_length=300, verbose_name="Секретный ключ")
    public_key = models.CharField(max_length=300, verbose_name="Публичный ключ")
    btcaddress = models.CharField(max_length=300, verbose_name="Адрес кошелька Bitcoin")


class ActiveDeals(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

class FinishedDeals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=now, verbose_name="Дата")
    bank = models.CharField(max_length=200, default='Нет', verbose_name="Банк")
    partner = models.CharField(max_length=30, verbose_name="Покупатель/Продавец")
    price = models.FloatField(max_length=200, default=0, verbose_name="Сумма")
    quantity = models.FloatField(max_length=200, default=0, verbose_name="Крипта")
    status = models.CharField(max_length=30, default='Sent', verbose_name="Статус")









