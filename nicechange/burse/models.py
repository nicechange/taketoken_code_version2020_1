# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Profile(models.Model):
    user = models.OneToOneField(User,unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    history = models.BooleanField(default=True, blank=True)
    two = models.BooleanField(default=True, blank=True)
    trade_rules = models.TextField(max_length=60, null=True, verbose_name='Правила торговли')
    dealscount = models.IntegerField(default=0, verbose_name="Количество сделок")
    uniquedealscount = models.IntegerField(default=0, verbose_name="Количество уникальных сделок")
    dealscounttext = models.CharField(max_length=30, default="0")
    steptwo = models.BooleanField(default=False)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        pass