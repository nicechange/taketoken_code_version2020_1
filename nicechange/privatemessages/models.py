# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# Create your models here.

class Blocked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blocked = models.FloatField(null=True, verbose_name="Заблокировано")
    fee = models.FloatField(null=True, verbose_name="Комиссия")
    real = models.FloatField(null=True, verbose_name="Итого")

class Thread(models.Model):
    participants = models.ManyToManyField(User)
    last_message = models.DateTimeField(null=True, blank=True, db_index=True)
    deal_info = models.CharField(max_length=500, default='')
    twallet = models.CharField(max_length=150, default='')
    destwallet = models.CharField(max_length=150, default='')
    quantity = models.FloatField(max_length=150, default=0)
    bl = models.ForeignKey(Blocked, on_delete=models.CASCADE, null=True)

class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)

class Read(models.Model):
    read = models.BooleanField(default=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

def update_last_message_datetime(sender, instance, created, **kwargs):
    """
    Update Thread's last_message field when
    a new message is sent.
    """
    if not created:
        return

    Thread.objects.filter(id=instance.thread.id).update(
        last_message=instance.datetime
    )

post_save.connect(update_last_message_datetime, sender=Message)

class ThreadActivity(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

class TestFlags(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    flagIsBalanceCorrect = models.BooleanField(default=True, db_index=True)
    flagIsCryptaSended = models.BooleanField(default=False, db_index=True)
    flagIsCryptaTaked = models.BooleanField(default=False, db_index=True)

