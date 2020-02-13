# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from django.forms import ModelForm, Form
from accounts.models import Notifications, Admins, Promo
from django import forms

class CreateUserForm(UserCreationForm):
    broker = fields.BooleanField(required=False)
    class Meta:
        model = User
        fields = ("username", "email",)

class PromoForm(ModelForm):
    class Meta:
        model = Promo
        fields = ("code", "action", "date")


class NotificationsForm(ModelForm):
    class Meta:
        model = Notifications
        fields = ("post", "reply", "chat", "deal", "support")

class PrepareFirstForm(Form):
    CHOICES = [('broker', 'Брокер'),
               ('user', 'Пользователь')]
    key = forms.CharField(label="Или ваш ключ для генерации одноразовых паролей (дезактивирует QR-код)  ",
                          max_length='200', required=False)
    type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), label='Выберите тип аккаунта')

class CodeAuthForm(Form):
    code = forms.CharField(max_length=200,
        label=("Код"),
    )

class LoginForm(Form):
    email = forms.CharField(max_length=200,
        label=("Email"),
    )
    password = forms.CharField(max_length=200,
                            label=("Пароль"),
                            )


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name","email")


class RspwnForm(Form):
    login = forms.CharField(max_length=200,
        label=("Введите свой логин, и мы вышлем вам новый пароль на ваш почтовый ящик."),
    )

class AdminsForm(ModelForm):
    class Meta:



        model = Admins
        fields = ("percent", "address")
