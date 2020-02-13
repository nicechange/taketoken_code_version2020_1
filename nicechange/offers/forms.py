# coding: utf-8
from django.forms import ModelForm, Form
from offers.models import Order, Offer, Proffer, Reply, Course
from django import forms
from accounts.models import Promo
class AddOrderForm(ModelForm):
        class Meta:
            model = Order
            fields = ( "offer_type", "quantity", "fiat", "sellorbuy", "bank", )


class AddProfferForm(ModelForm):
    class Meta:
        model = Proffer
        fields = ("rate", "min", "max", "bank_sber", "bank_tinkoff", "bank_vtb", "bank_promsvyaz", 'bank_alfa', 'bank_qiwi', 'bank_yandex', 'info')


class AddOfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ("quantity", )

class AddReplyForm(ModelForm):
    sum = forms.FloatField
    class Meta:
        model = Reply
        fields = ("quantity", )
TOKEN_CHOICES = (("Bitcoin", "Bitcoin"), ("Etherium", "Etherium"))

class TransactionForm(Form):
    quantity = forms.FloatField(label='Количество монет')
    address = forms.CharField(max_length=100, label='Адрес получателя')


class AddCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ("burse", "type_of_token", "sellorbuy", "percent", )

class SearchForm(ModelForm):
    class Meta:
        model = Proffer
        fields = ("rate", "bank_search", )

class DealForm(Form):
     None

class PromoUserForm(ModelForm):
    class Meta:
        model = Promo
        fields = ("code",)

from django import forms

class DateForm(forms.Form):
    MONTHS = {
    1:('янв'), 2:('фев'), 3:('мар'), 4:('апр'),
    5:('май'), 6:('июн'), 7:('июл'), 8:('авг'),
    9:('сен'), 10:('окт'), 11:('ноя'), 12:('дек')
}
    date1 = forms.DateField(widget=forms.SelectDateWidget(months=MONTHS))
    date2 = forms.DateField(widget=forms.SelectDateWidget(months=MONTHS))