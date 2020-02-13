# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import EmailValidator

class FutureUser(models.Model):
    email = models.EmailField(max_length=30, validators=[EmailValidator],
                              error_messages={'invalid': 'Введите адрес ящика для подписки.'})

class CBit(models.Model):
    name = models.CharField(max_length=200, default='')
    link = models.CharField(max_length=200, default='')
    pay = models.CharField(max_length=200, default='')
    get = models.CharField(max_length=200, default='')
    reserve = models.CharField(max_length=200, default='')
    mode = models.CharField(max_length=200, default='')

class CLite(models.Model):
    name = models.CharField(max_length=200, default='')
    link = models.CharField(max_length=200, default='')
    pay = models.CharField(max_length=200, default='')
    get = models.CharField(max_length=200, default='')
    reserve = models.CharField(max_length=200, default='')
    mode = models.CharField(max_length=200, default='')

class CEther(models.Model):
    name = models.CharField(max_length=200, default='')
    link = models.CharField(max_length=200, default='')
    pay = models.CharField(max_length=200, default='')
    get = models.CharField(max_length=200, default='')
    reserve = models.CharField(max_length=200, default='')
    mode = models.CharField(max_length=200, default='')
