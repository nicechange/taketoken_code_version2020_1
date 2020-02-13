# -*- coding: utf-8 -*-
import django_tables2

from presentation.models import CBit, CLite, CEther


class CourseBitTable(django_tables2.Table):
    name = django_tables2.TemplateColumn(verbose_name="Обменник:", template_code='<a target="_blank" href="{{record.link}}">{{record.name}}</a>')
    pay = django_tables2.Column(verbose_name="Отдаете:")
    get = django_tables2.Column(verbose_name="Получаете(руб.):")
    #reserve = django_tables2.Column(verbose_name="Остаток(руб.):")
    #mode = django_tables2.Column(verbose_name="Отзывы:")
    class Meta:
        attrs = {"class": "table table-sm-down", }   # this fixed table rendering
        model = CBit
        fields = ("name", "pay", "get")

class CourseLiteTable(django_tables2.Table):
    name = django_tables2.TemplateColumn(verbose_name="Обменник:", template_code='<a target="_blank" href="{{record.link}}">{{record.name}}</a>')
    pay = django_tables2.Column(verbose_name="Отдаете:")
    get = django_tables2.Column(verbose_name="Получаете(руб.):")
    #reserve = django_tables2.Column(verbose_name="Остаток(руб.):")
    #mode = django_tables2.Column(verbose_name="Отзывы:")
    class Meta:
        attrs = {"class": "table table-sm-down", }   # this fixed table rendering
        model = CLite
        fields = ("name", "pay", "get")

class CourseEtherTable(django_tables2.Table):
    name = django_tables2.TemplateColumn(verbose_name="Обменник:", template_code='<a target="_blank" href="{{record.link}}">{{record.name}}</a>')
    pay = django_tables2.Column(verbose_name="Отдаете:")
    get = django_tables2.Column(verbose_name="Получаете(руб.):")
    #reserve = django_tables2.Column(verbose_name="Остаток(руб.):")
    #mode = django_tables2.Column(verbose_name="Отзывы:")
    class Meta:
        attrs = {"class": "table table-sm-down", }   # this fixed table rendering
        model = CEther
        fields = ("name", "pay", "get")