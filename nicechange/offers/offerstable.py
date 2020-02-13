# -*- coding: utf-8 -*-
import django_tables2
from  django_tables2 import A
from offers.models import Offer, Reply, FinishedDeals
from offers.deals import deal_start_order, deal_start_proffer


class MyOffersTable(django_tables2.Table):
    offers = django_tables2.LinkColumn(deal_start_order, text='deal', args=[A('pk')])
    class Meta:
        attrs = {"class": "paleblue", }   # this fixed table rendering
        model = Offer
        fields = ("quantity", "information")

class MyRepliesTable(django_tables2.Table):
    replies = django_tables2.LinkColumn(deal_start_proffer, text='Сделка', args=[A('pk')], verbose_name='Действия')
    class Meta:
        attrs = {"class": "paleblue", }   # this fixed table rendering
        model = Reply
        fields = ("user", "sellorbuy", "quantity", )

class MyFDTable(django_tables2.Table):
    class Meta:
        attrs = {"class": "paleblue", }   # this fixed table rendering
        model = FinishedDeals
        fields = ("id", "partner", "price", "status", "user_id", "date", "quantity", "bank")

