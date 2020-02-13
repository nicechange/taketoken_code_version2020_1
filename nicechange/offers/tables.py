# -*- coding: utf-8 -*-
import django_tables2
from django_tables2.utils import A
from offers.models import Order, Proffer, Wallet
from offers.myoffers import my_offers, my_replies
from offers.myoffers import publish_order, publish_proffer, delete_course, open_wallet, delete_wallet, select_wallet
from offers.models import Course
class MyOrdersTable(django_tables2.Table):
    offers = django_tables2.LinkColumn(my_offers, text=lambda record: str(record.offers_count) +
                                                                      ' offers',  args=[A('pk')])
    class Meta:
        attrs = {"class": "table table-condensed table-striped footable table-hover", }   # this fixed table rendering
        model = Order
        fields = ("status", "sellorbuy", "date", "offer_type", "quantity", "fiat")

class MyProffersTable(django_tables2.Table):
    replies = django_tables2.LinkColumn(my_replies, text=lambda record: str(record.replies_count) +
                                                                      ' replies',  args=[A('pk')])
    class Meta:
        attrs = {"class": "table table-condensed table-striped footable table-hover", }   # this fixed table rendering
        model = Proffer
        fields = ("type", "owner", "status", "type_of_token", "date", "rate" )

class MyOrdersTableDraft(django_tables2.Table):
    action = django_tables2.LinkColumn(publish_order, text='publish',  args=[A('pk')])
    class Meta:
        attrs = {"class": "table table-condensed table-striped footable table-hovere", }   # this fixed table rendering
        model = Order
        fields = ("owner", "status", "sellorbuy", "date", "offer_type",  "quantity", "fiat")

class MyProffersTableDraft(django_tables2.Table):
    action = django_tables2.LinkColumn(publish_proffer, text='Опубликовать',  args=[A('pk')], verbose_name='Действие')
    class Meta:
        attrs = {"class": "table table-condensed table-striped footable table-hover", }   # this fixed table rendering
        model = Proffer
        fields = ("status", "date", "type", "rate" )

class CoursesTable(django_tables2.Table):
    action = django_tables2.LinkColumn(delete_course, text='delete',  args=[A('pk')])
    class Meta:
        attrs = {"class": "paleblue", }   # this fixed table rendering
        model = Course
        fields = ("burse", "type_of_token", "sellorbuy", "percent", )

class WalletsTable(django_tables2.Table):
    action = django_tables2.LinkColumn(open_wallet, text='open',  args=[A('pk')])
    moving = django_tables2.LinkColumn(delete_wallet, text='delete',  args=[A('pk')])
    class Meta:
        attrs = {"class": "paleblue", }   # this fixed table rendering
        model = Wallet
        fields = ("btcaddress", "ethaddress", "btcbalance", "ethbalance",)

class DealWalletsTable(django_tables2.Table):
    action = django_tables2.LinkColumn(select_wallet, text='Выбрать',  args=[A('pk')], verbose_name='Действие')
    class Meta:
        attrs = {"class": "paleblue", }   # this fixed table rendering
        model = Wallet
        fields = ("btcaddress", "btcbalance",)

