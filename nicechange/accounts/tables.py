# -*- coding: utf-8 -*-
import django_tables2
from django_tables2.utils import A
from offers.models import Order, Proffer
from offers.views import  answer
from accounts.models import Promo

#class OrdersTable(django_tables2.Table):
 #   order = django_tables2.LinkColumn(reply, text='Ответить', args=[A('pk')], verbose_name= 'Действие')
  #  class Meta:
   #     attrs = {"class": "paleblue", }   # this fixed table rendering
    #    model = Order
     #   fields = ("owner", "status", "sellorbuy", "date", "offer_type", "quantity",  "fiat")

class CodesTable(django_tables2.Table):
    #proffer = django_tables2.LinkColumn(answer, text='Ответить', args=[A('pk')], verbose_name= 'Действие')
    class Meta:
        attrs = {"class": "table table-condensed table-striped footable table-hover", }    # this fixed table rendering
        model = Promo
        fields = ("code","action", "date", "used",)

