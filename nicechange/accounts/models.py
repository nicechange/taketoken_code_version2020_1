# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Notifications(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    post = models.BooleanField(default=True, verbose_name="После размещения предложения")
    reply = models.BooleanField(default=True, verbose_name="После ответа на ваше предложение")
    chat = models.BooleanField(default=True, verbose_name="После начала чата")
    deal = models.BooleanField(default=True, verbose_name="После начала сделки")
    support = models.BooleanField(default=True, verbose_name="Уведомления поддержки")

class AlreadyEnter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=200, default='')

class Admins(models.Model):
    percent = models.FloatField(null=True, verbose_name="Процент от сделки")
    address = models.CharField(max_length=200, default='', verbose_name="Адрес единственного кошелька для отчислений")
    sum = models.FloatField(null=True, verbose_name="Сумма всех сделок")
    walletsum = models.FloatField(null=True, verbose_name="Сумма на кошельке в данный момент")
    count = models.FloatField(null=True, verbose_name="Количество всех сделок")

class Promo(models.Model):#Сверить с кодом с офисного компа
    code = models.CharField(max_length=200, null=True, verbose_name="Промо-код")
    action = models.CharField(max_length=200, null=True, verbose_name="Название акции")
    date = models.DateField(max_length=200, default=now, verbose_name="Дата")
    used = models.BooleanField(max_length=200, default=False, verbose_name="Использован")

