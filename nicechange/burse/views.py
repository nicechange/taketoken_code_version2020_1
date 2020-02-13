# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from offers.models import Order, Proffer
from burse.tables import  ProffersTable
from offers.forms import SearchForm
from online_users.models import OnlineUserActivity
from offers.models import Wallet, Reply
from privatemessages.models import Thread
import datetime
import threading
from offers.burses import update
from django.conf import global_settings
def main_page(request, forbidden = '', usr = None):
    error_message = ''
    nothing = 'false'
    threading.Thread(target=update).start()
    forbidden = forbidden
    if forbidden:
        if forbidden == 'forbidden':
            error_message = 'К сожалению, это предложение устарело!'
        else:
            if forbidden == 'own':
                error_message = 'Ответить на свое предложение невозможно!'
    mainbalance = 0.0
    balance = ''
    if not request.user.is_anonymous:
        wallets = Wallet.objects.filter(user=request.user)
        for w in wallets:
            mainbalance += float(w.btcbalance)
        balance = str(mainbalance) + ' BTC'
        finishdate = datetime.datetime.now() - datetime.timedelta(hours=1, minutes=30)
        for ans in Reply.objects.filter(user=request.user):
            if ans.time < finishdate.time():
                proffer = ans.proffer
                proffer.replies_count = proffer.replies_count - 1
                proffer.save()
                if ans.thread:
                    thread = Thread.objects.filter(id=ans.thread.id)
                    thread.delete()
                ans.delete()

    online_users = []
    from datetime import timedelta
    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=60))
    active_users = (user for user in user_activity_objects)
    for u in active_users:
        online_users.append(u.user)
    user = request.user
    searchoff = 'true'
    search_form = None
    test = None
    bank = ''
    rate = 0
    count = 15
    mode = 'КУПЛЮ'
    search_table =  ProffersTable(Proffer.objects.all())
    #orders_ltc = OrdersTable(Order.objects.filter(offer_type__contains="LTC").exclude(state="Draft"))
    #orders_xmr = OrdersTable(Order.objects.filter(offer_type__contains="XMR").exclude(state="Draft"))
    #orders_dash = OrdersTable(Order.objects.filter(offer_type__contains="DASH").exclude(state="Draft"))
    #orders_eth = OrdersTable(Order.objects.filter(offer_type__contains="ETH").exclude(state="Draft"))
    #orders_zec = OrdersTable(Order.objects.filter(offer_type__contains="ZEC").exclude(state="Draft"))
    #orders_btc = OrdersTable(Order.objects.filter(offer_type__contains="BTC").exclude(state="Draft"))
    proffers_ltc = ProffersTable(Proffer.objects.filter(type_of_token__contains="LTC").exclude(state="Draft"))
    proffers_xmr = ProffersTable(Proffer.objects.filter(type_of_token__contains="XMR").exclude(state="Draft"))
    proffers_dash = ProffersTable(Proffer.objects.filter(type_of_token__contains="DASH").exclude(state="Draft"))
    proffers_eth = ProffersTable(Proffer.objects.filter(type_of_token__contains="ETH").exclude(state="Draft"))
    proffers_zec = ProffersTable(Proffer.objects.filter(type_of_token__contains="ZEC").exclude(state="Draft"))
    if usr:
        proffers_btc_buy = ProffersTable(Proffer.objects.filter(user=usr, type_of_token__contains="BTC", type='КУПЛЮ').exclude(state="Draft")[::-1])
        proffers_btc_sale = ProffersTable(
            Proffer.objects.filter(user=usr, type_of_token__contains="BTC", type='ПРОДАМ').exclude(state="Draft")[::-1])
    else:
        proffers_btc_buy = ProffersTable(
            Proffer.objects.filter(type_of_token__contains="BTC", type='КУПЛЮ').exclude(state="Draft")[::-1])
        proffers_btc_sale = ProffersTable(
            Proffer.objects.filter(type_of_token__contains="BTC", type='ПРОДАМ').exclude(state="Draft")[::-1])
    search_form = SearchForm()
    for obj in Proffer.objects.all():
        sum = 0
        for wlt in Wallet.objects.filter(user=obj.user):
             sum += float(wlt.btcbalance)
        obj.balance = sum * obj.rate
        obj.save()
    if request.method == 'POST':
        if "buy_more" in request.POST:
            proffers_btc_sale = ProffersTable(
                Proffer.objects.filter(type_of_token__contains="BTC", type='ПРОДАМ').exclude(state="Draft"))
        if "sale_more" in request.POST:
            proffers_btc_buy = ProffersTable(
                Proffer.objects.filter(type_of_token__contains="BTC", type='КУПЛЮ').exclude(state="Draft"))
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            rate = search_form.data['rate']
            bank = search_form.cleaned_data['bank_search']
            searchoff = 'false'
            if 'buybutton' in search_form.data:
                mode = 'КУПЛЮ'
            else:
                mode = 'ПРОДАМ'
            if Proffer.objects.filter(max__gte=int(rate), min__lte=int(rate), bank__contains=bank, type=mode).count() == 0:
                nothing = 'true'
            else:
                search_table = ProffersTable(Proffer.objects.filter(max__gte=int(rate), min__lte=int(rate), bank__contains=bank, type=mode ))

    return render(request, 'index_main.html', {


                                           'proffers_ltc': proffers_ltc, 'proffers_xmr': proffers_xmr,
                                           'proffers_dash': proffers_dash, 'proffers_eth': proffers_eth,
                                           'proffers_zec': proffers_zec, 'proffers_btc_buy': proffers_btc_buy,
                                               'proffers_btc_sale': proffers_btc_sale,
                                               'search_table':search_table,
                                           'user':user,
                                               'searchoff':searchoff,
                                               'search_form':search_form,
                                               'bank':bank,
                                               'rate':rate,
                                               'mode':mode,
                                               'online_users':online_users,
                                               'balance':balance,
                                               'forbidden':forbidden,
                                               'error_message':error_message,
                                               'nothing':nothing
                                           })


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from burse.models import Profile
from burse.forms import UserForm,ProfileForm
from django.contrib import messages
from templated_email import send_templated_mail
@login_required
@transaction.atomic
def update_profile(request):
    user_form = UserForm(request.POST, instance=request.user)
    profile_form = ProfileForm(request.POST, instance=request.user.profile)
    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            user = request.user
            npswd = request.POST.get('password')
            if npswd != '':
                send_templated_mail(
                    template_name="rspwn.html",
                    from_email='from@example.com',
                    recipient_list=[user.email],
                    context={
                        'password': npswd
                    },

                )
                user.set_password(request.POST.get('password'))
            user.save()
        else:
            return HttpResponseRedirect('/nicechange/')
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def stat(request, user = None):
    user = User.objects.get(id=user)
    date = user.date_joined
    user_name = user.username
    profile = Profile.objects.get(user=user)
    deals = profile.dealscount
    unique = profile.uniquedealscount
    return render(request, 'stats.html', {
       'date': date, 'user_name':user_name, 'deals':deals, 'unique':unique, 'usr':user
    })

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/nicechange/')
