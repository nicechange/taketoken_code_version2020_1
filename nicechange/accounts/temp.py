# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, group_required
from django.contrib.auth.models import User
from offers.forms import AddOrderForm, AddOfferForm, AddProfferForm,AddReplyForm, TransactionForm, AddCourseForm
from django.http import HttpResponseRedirect
from offers.models import Order, Proffer, Course, BurseCourse, Wallet, DealRole
from offers.tables import MyOrdersTable, MyProffersTable, MyOrdersTableDraft, MyProffersTableDraft, CoursesTable, WalletsTable, DealWalletsTable
from privatemessages.models import Read
from blockchain import wallet
from offers.burses import update
from bitcoin import *

import socket
import bitcoinrpc
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import threading
from decimal import *
import time

def add_order(request):
    if not (request.user.is_authenticated()):
        return HttpResponseRedirect('/login/')
    if (request.user.groups.filter(name='broker').exists()):
        return HttpResponseRedirect('/login/')
    form = AddOrderForm
    user=request.user
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            if (request.user.groups.filter(name='broker').exists()):
                order.owner = request.user.username
            order.save()
            users = User.objects.all()
            from templated_email import send_templated_mail
            threading.Thread(target=send_templated_mail, args=("putorder.html",
                                                               'from@example.com',
                                                               [user.email],
                                                               {
                                                                   'username': request.user.username,
                                                                   'token': order.offer_type,
                                                                   'buysale': order.sellorbuy,
                                                                   'quantity': order.quantity
                                                               }
                                                               )).start()
            return HttpResponseRedirect('/cabinet/')
    return render(request, 'addorder.html',  {'form': form,})

@group_required("broker", login_url='/login/')
def add_proffer(request):
    threading.Thread(target=update).start()
    if not (request.user.is_authenticated()):
        return HttpResponseRedirect('/login/')
    form = AddProfferForm
    user = request.user
    condition = Course.objects.filter(user=request.user, sellorbuy='ПОКУПКА', type_of_token='BTC').last()
    if condition:
        crs = float(BurseCourse.objects.filter(burse=Course.objects.filter(user=request.user,
                                                                                      sellorbuy='ПОКУПКА', type_of_token='BTC').last().burse, token='BTC').last().course)
        course_btc_buy = crs - (crs / 100 * condition.percent)
    else:
        course_btc_buy = 0
    condition = Course.objects.filter(user=request.user, sellorbuy='ПРОДАЖА', type_of_token='BTC').last()
    if condition:
        crs = float(BurseCourse.objects.filter(burse=Course.objects.filter(user=request.user,
                                                                                       sellorbuy='ПРОДАЖА', type_of_token='BTC').last().burse, token='BTC').last().course)
        course_btc_sale = crs + (crs / 100 * condition.percent)
    else:
        course_btc_sale = 0
    condition = Course.objects.filter(user=request.user, sellorbuy='ПОКУПКА', type_of_token='ETH').last()
    if condition:
        crs = float(BurseCourse.objects.filter(burse=Course.objects.filter(user=request.user,
                                                                                      sellorbuy='ПОКУПКА', type_of_token='ETH').last().burse,  token='ETH').last().course)
        course_eth_buy = crs - (crs / 100 * condition.percent)
    else:
        course_eth_buy = 0
    condition = Course.objects.filter(user=request.user, sellorbuy='ПРОДАЖА', type_of_token='ETH').last()
    if condition:
        crs = float(BurseCourse.objects.filter(burse=Course.objects.filter(user=request.user,
                                                                                       sellorbuy='ПРОДАЖА', type_of_token='ETH').last().burse, token='ETH').last().course)
        course_eth_sale = crs + (crs / 100 * condition.percent)
    else:
        course_eth_sale = 0
    condition = Course.objects.filter(user=request.user, sellorbuy='ПОКУПКА', type_of_token='LTC').last()
    if condition:
        crs = float(BurseCourse.objects.filter(burse=Course.objects.filter(user=request.user,
                                                                                      sellorbuy='ПОКУПКА', type_of_token='LTC').last().burse, token='LTC').last().course)
        course_ltc_buy = crs - (crs / 100 * condition.percent)
    else:
        course_ltc_buy = 0
    condition = Course.objects.filter(user=request.user, sellorbuy='ПРОДАЖА', type_of_token='LTC').last()
    if condition:
        crs = float(BurseCourse.objects.filter(burse=Course.objects.filter(user=request.user,
                                                                                       sellorbuy='ПРОДАЖА', type_of_token='LTC').last().burse, token='LTC').last().course)
        course_ltc_sale = crs + (crs / 100 * condition.percent)
    else:
        course_ltc_sale = 0

    if request.method == 'POST':
        form = AddProfferForm(request.POST)
        if form.is_valid():
            proffer = form.save(commit=False)
            proffer.user = request.user
            if (request.user.groups.filter(name='broker').exists()):
                proffer.owner = request.user.username
            proffer.save()
            users = User.objects.all()
            from templated_email import send_templated_mail
            threading.Thread(target=send_templated_mail, args=("putoffer.html", 'from@example.com',
                                                               [user.email],
                                                               {
                                                                   'username': user.username,
                                                                   'token': proffer.type_of_token,
                                                                   'buy': proffer.buy,
                                                                   'sale': proffer.sale
                                                               }
                                                               )).start()

            #for user in users:
                #mailer.send('Уведомление', 'shnicechange@gmail.com')
            return HttpResponseRedirect('/cabinet/')
    return render(request, 'addproffer.html',  {'form': form, 'course_btc_buy': course_btc_buy, 'course_btc_sale': course_btc_sale,
                                                'course_eth_buy': course_eth_buy,
                                                'course_eth_sale': course_eth_sale,
                                                'course_ltc_buy': course_ltc_buy, 'course_ltc_sale': course_ltc_sale})

@login_required(login_url='/login/')
@group_required("broker", login_url='/login/')
def reply(request, item_id):
    threading.Thread(target=update).start()
    form = AddOfferForm
    order = Order.objects.get(id=item_id)
    user = order.user
    deals = 0
    reviews = 0
    usr = request.user
    offer_type = order.offer_type
    condition = Course.objects.filter(type_of_token=offer_type, user=request.user, sellorbuy=order.sellorbuy).last()
    if condition:
        crs = 0
        crs = BurseCourse.objects.filter(burse=condition.burse, token=offer_type).last().course
        if order.sellorbuy == 'ПРОДАЖА':
            course = float(crs) - (float(crs)/100 * condition.percent)
        else:
            course = float(crs) + (float(crs)/100 * condition.percent)
    else:
        course = 0
    if request.method == 'POST':
        form = AddOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            order = Order.objects.get(id=item_id)
            offer.order = order
            order.offers_count = order.offers_count + 1
            offer.information = "Брокер " + usr.username + "Сделок:0"
            order.save()
            offer.save()
            from templated_email import send_templated_mail
            threading.Thread(target=send_templated_mail, args=("rorder2.html",
                             'from@example.com',
                             [request.user.email],
                             {
                                 'username': user.username,
                                 'token': order.offer_type,
                                 'buysale': order.sellorbuy,
                                 'quantity': order.quantity
                             })
                             ).start()

            threading.Thread(target=send_templated_mail, args=("rorder1.html",
                                                               'from@example.com',
                                                               [order.user.email],
                                                               {
                                                                   'username': user.username,
                                                                   'token': order.offer_type,
                                                                   'buysale': order.sellorbuy,
                                                                   'quantity': order.quantity
                                                               }
                                                               )).start()
            return HttpResponseRedirect('/index/')
    return render(request, 'addoffer.html', {'form': form, 'id':item_id, 'offer_type':offer_type, 'deals':deals, 'reviews':reviews, 'broker':user,
                                             'bank':order.bank, 'quantity': order.quantity, 'course':course, 'buysale': order.sellorbuy})

@login_required(login_url='/login/')
def answer(request, item_id):
    form = AddReplyForm
    proffer = Proffer.objects.get(id=item_id)
    user_id = proffer.user.id
    buy = proffer.buy
    sale = proffer.sale
    user = request.user
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            proffer = Proffer.objects.get(id=item_id)
            reply.proffer = proffer
            proffer.replies_count = proffer.replies_count + 1
            proffer.save()
            reply.save()
            from templated_email import send_templated_mail
            threading.Thread(target=send_templated_mail, args=("roffer2.html",
                                                               'from@example.com',
                                                               [request.user.email],
                                                               {
                                                                   'username': user.username,
                                                                   'token': proffer.type_of_token,
                                                                   'buy': proffer.buy,
                                                                   'sale': proffer.sale
                                                               }
                                                               ) ).start()

            threading.Thread(target=send_templated_mail, args=("roffer1.html",
                                                               )).start()
            send_templated_mail(
                template_name="roffer1.html",
                from_email='from@example.com',
                recipient_list=[proffer.user.email],
                context={
                    'username': user.username,
                    'token': proffer.type_of_token,
                    'buy': proffer.buy,
                    'sale': proffer.sale
                },

            )
            return HttpResponseRedirect('/index/')
    return render(request, 'answer.html', {'user_id':user_id, 'form': form, 'id':item_id, 'buy':buy, 'sale':sale, 'buystrip':buy.strip('$').replace(' ',''),
                                           'salestrip':sale.strip('$').replace(' ','')})



def transaction_old(request):
    form = TransactionForm
    priv = sha256('rsdth#vaecsKVKrgawesdfg%#@rgser23463aga')
    pub = privtopub(priv)
    addr = pubtoaddr(pub)
    h = history(addr)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
             outs = [{'value': int(form.cleaned_data['quantity']), 'address': form.cleaned_data['address'].__str__()}]
             tx = mktx(h, outs)
             tx_ = sign(tx, 0, priv)
             #tr = Transactions(testnet=True)
             #tr.push(tx=tx_)
             bytetx = tx_
             pushtx(bytetx)
    return render(request, 'transaction.html', {'form': form, 'new_wallet':addr})

def my_orders(request):
    if not (request.user.is_authenticated()):
        return HttpResponseRedirect('/login/')
    orders_ltc = MyOrdersTable(Order.objects.filter(offer_type__contains="LTC", user=request.user))
    orders_xmr = MyOrdersTable(Order.objects.filter(offer_type__contains="XMR", user=request.user))
    orders_dash = MyOrdersTable(Order.objects.filter(offer_type__contains="DASH", user=request.user))
    orders_eth = MyOrdersTable(Order.objects.filter(offer_type__contains="ETH", user=request.user))
    orders_zec = MyOrdersTable(Order.objects.filter(offer_type__contains="ZEC", user=request.user))
    orders_btc = MyOrdersTable(Order.objects.filter(offer_type__contains="BTC", user=request.user))
    return render(request, 'myorders.html', {'orders_ltc': orders_ltc, 'orders_xmr': orders_xmr,
                                           'orders_dash': orders_dash, 'orders_eth': orders_eth,
                                           'orders_zec': orders_zec, 'orders_btc': orders_btc})


@login_required(login_url='/login/')
def cabinet(request):
    if (request.user.groups.filter(name='broker').exists()):
        return HttpResponseRedirect('/broker/')
    else:
        return HttpResponseRedirect('/user/')


def user(request):
    if not (request.user.is_authenticated()):
        return HttpResponseRedirect('/login/')
    orders_ltc = MyOrdersTable(Order.objects.filter(offer_type__contains="LTC", user=request.user).exclude(state="Draft"))
    orders_xmr = MyOrdersTable(Order.objects.filter(offer_type__contains="XMR", user=request.user).exclude(state="Draft"))
    orders_dash = MyOrdersTable(Order.objects.filter(offer_type__contains="DASH", user=request.user).exclude(state="Draft"))
    orders_eth = MyOrdersTable(Order.objects.filter(offer_type__contains="ETH", user=request.user).exclude(state="Draft"))
    orders_zec = MyOrdersTable(Order.objects.filter(offer_type__contains="ZEC", user=request.user).exclude(state="Draft"))
    orders_btc = MyOrdersTable(Order.objects.filter(offer_type__contains="BTC", user=request.user).exclude(state="Draft"))

    orders_ltc_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="LTC", user=request.user, state="Draft"))
    orders_xmr_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="XMR", user=request.user, state="Draft"))
    orders_dash_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="DASH", user=request.user, state="Draft"))
    orders_eth_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="ETH", user=request.user, state="Draft"))
    orders_zec_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="ZEC", user=request.user, state="Draft"))
    orders_btc_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="BTC", user=request.user, state="Draft"))
    threads = Read.objects.filter(user=request.user)
    read = True
    for th in threads:
        if th.read == False:
            read = False
    if not read:
        messages = 'Есть непрочитанные.'
    else:
        messages = 'Непрочитанных нет.'
    return render(request, 'user.html', {'orders_ltc': orders_ltc, 'orders_xmr': orders_xmr,
                                           'orders_dash': orders_dash, 'orders_eth': orders_eth,
                                           'orders_zec': orders_zec, 'orders_btc': orders_btc,
                                         'orders_ltc_draft': orders_ltc_draft, 'orders_xmr_draft': orders_xmr_draft,
                                         'orders_dash_draft': orders_dash_draft, 'orders_eth_draft': orders_eth_draft,
                                         'orders_zec_draft': orders_zec_draft, 'orders_btc_draft': orders_btc_draft,
                                         'user': request.user,
                                         'messages':messages})

@group_required("broker", login_url='/login/')
def my_for_broker(request):
    if not (request.user.is_authenticated()):
        return HttpResponseRedirect('/login/')
    orders_ltc = MyOrdersTable(Order.objects.filter(offer_type__contains="LTC", user=request.user).exclude(state="Draft"))
    orders_xmr = MyOrdersTable(Order.objects.filter(offer_type__contains="XMR", user=request.user).exclude(state="Draft"))
    orders_dash = MyOrdersTable(Order.objects.filter(offer_type__contains="DASH", user=request.user).exclude(state="Draft"))
    orders_eth = MyOrdersTable(Order.objects.filter(offer_type__contains="ETH", user=request.user).exclude(state="Draft"))
    orders_zec = MyOrdersTable(Order.objects.filter(offer_type__contains="ZEC", user=request.user).exclude(state="Draft"))
    orders_btc = MyOrdersTable(Order.objects.filter(offer_type__contains="BTC", user=request.user).exclude(state="Draft"))
    proffers_ltc = MyProffersTable(Proffer.objects.filter(type_of_token__contains="LTC", user=request.user).exclude(state="Draft"))
    proffers_xmr = MyProffersTable(Proffer.objects.filter(type_of_token__contains="XMR", user=request.user).exclude(state="Draft"))
    proffers_dash = MyProffersTable(Proffer.objects.filter(type_of_token__contains="DASH", user=request.user).exclude(state="Draft"))
    proffers_eth = MyProffersTable(Proffer.objects.filter(type_of_token__contains="ETH", user=request.user).exclude(state="Draft"))
    proffers_zec = MyProffersTable(Proffer.objects.filter(type_of_token__contains="ZEC", user=request.user).exclude(state="Draft"))
    proffers_btc = MyProffersTable(Proffer.objects.filter(type_of_token__contains="BTC", user=request.user).exclude(state="Draft"))

    orders_ltc_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="LTC", user=request.user, state="Draft"))
    orders_xmr_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="XMR", user=request.user, state="Draft"))
    orders_dash_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="DASH", user=request.user, state="Draft"))
    orders_eth_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="ETH", user=request.user, state="Draft"))
    orders_zec_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="ZEC", user=request.user, state="Draft"))
    orders_btc_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="BTC", user=request.user, state="Draft"))
    proffers_ltc_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="LTC", user=request.user, state="Draft"))
    proffers_xmr_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="XMR", user=request.user, state="Draft"))
    proffers_dash_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="DASH", user=request.user, state="Draft"))
    proffers_eth_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="ETH", user=request.user, state="Draft"))
    proffers_zec_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="ZEC", user=request.user, state="Draft"))
    proffers_btc_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="BTC", user=request.user, state="Draft"))

    return render(request, 'index_.html', {'orders_ltc': orders_ltc, 'orders_xmr': orders_xmr,
                                           'orders_dash': orders_dash, 'orders_eth': orders_eth,
                                           'orders_zec': orders_zec, 'orders_btc': orders_btc,
                                           'proffers_ltc': proffers_ltc, 'proffers_xmr': proffers_xmr,
                                           'proffers_dash': proffers_dash, 'proffers_eth': proffers_eth,
                                           'proffers_zec': proffers_zec, 'proffers_btc': proffers_btc,
                                           'orders_ltc_draft': orders_ltc_draft, 'orders_xmr_draft': orders_xmr_draft,
                                           'orders_dash_draft': orders_dash_draft, 'orders_eth_draft': orders_eth_draft,
                                           'orders_zec_draft': orders_zec_draft, 'orders_btc_draft': orders_btc_draft,
                                           'proffers_ltc_draft': proffers_ltc_draft, 'proffers_xmr_draft': proffers_xmr_draft,
                                           'proffers_dash_draft': proffers_dash_draft, 'proffers_eth_draft': proffers_eth_draft,
                                           'proffers_zec_draft': proffers_zec_draft, 'proffers_btc_draft': proffers_btc_draft
                                           })

@group_required("broker", login_url='/login/')
def broker(request):
    if not (request.user.is_authenticated()):
        return HttpResponseRedirect('/login/')
    orders_ltc = MyOrdersTable(Order.objects.filter(offer_type__contains="LTC", user=request.user).exclude(state="Draft"))
    orders_xmr = MyOrdersTable(Order.objects.filter(offer_type__contains="XMR", user=request.user).exclude(state="Draft"))
    orders_dash = MyOrdersTable(Order.objects.filter(offer_type__contains="DASH", user=request.user).exclude(state="Draft"))
    orders_eth = MyOrdersTable(Order.objects.filter(offer_type__contains="ETH", user=request.user).exclude(state="Draft"))
    orders_zec = MyOrdersTable(Order.objects.filter(offer_type__contains="ZEC", user=request.user).exclude(state="Draft"))
    orders_btc = MyOrdersTable(Order.objects.filter(offer_type__contains="BTC", user=request.user).exclude(state="Draft"))
    proffers_ltc = MyProffersTable(Proffer.objects.filter(type_of_token__contains="LTC", user=request.user).exclude(state="Draft"))
    proffers_xmr = MyProffersTable(Proffer.objects.filter(type_of_token__contains="XMR", user=request.user).exclude(state="Draft"))
    proffers_dash = MyProffersTable(Proffer.objects.filter(type_of_token__contains="DASH", user=request.user).exclude(state="Draft"))
    proffers_eth = MyProffersTable(Proffer.objects.filter(type_of_token__contains="ETH", user=request.user).exclude(state="Draft"))
    proffers_zec = MyProffersTable(Proffer.objects.filter(type_of_token__contains="ZEC", user=request.user).exclude(state="Draft"))
    proffers_btc = MyProffersTable(Proffer.objects.filter(type_of_token__contains="BTC", user=request.user).exclude(state="Draft"))

    orders_ltc_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="LTC", user=request.user, state="Draft"))
    orders_xmr_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="XMR", user=request.user, state="Draft"))
    orders_dash_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="DASH", user=request.user, state="Draft"))
    orders_eth_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="ETH", user=request.user, state="Draft"))
    orders_zec_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="ZEC", user=request.user, state="Draft"))
    orders_btc_draft = MyOrdersTableDraft(Order.objects.filter(offer_type__contains="BTC", user=request.user, state="Draft"))
    proffers_ltc_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="LTC", user=request.user, state="Draft"))
    proffers_xmr_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="XMR", user=request.user, state="Draft"))
    proffers_dash_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="DASH", user=request.user, state="Draft"))
    proffers_eth_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="ETH", user=request.user, state="Draft"))
    proffers_zec_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="ZEC", user=request.user, state="Draft"))
    proffers_btc_draft = MyProffersTableDraft(Proffer.objects.filter(type_of_token__contains="BTC", user=request.user, state="Draft"))
    threads = Read.objects.filter(user=request.user)
    read = True
    for th in threads:
        if th.read == False:
            read = False
    if not read:
        messages = 'Есть непрочитанные.'
    else:
        messages = 'Непрочитанных нет.'
    return render(request, 'broker.html', {'orders_ltc': orders_ltc, 'orders_xmr': orders_xmr,
                                           'orders_dash': orders_dash, 'orders_eth': orders_eth,
                                           'orders_zec': orders_zec, 'orders_btc': orders_btc,
                                           'proffers_ltc': proffers_ltc, 'proffers_xmr': proffers_xmr,
                                           'proffers_dash': proffers_dash, 'proffers_eth': proffers_eth,
                                           'proffers_zec': proffers_zec, 'proffers_btc': proffers_btc,
                                           'orders_ltc_draft': orders_ltc_draft, 'orders_xmr_draft': orders_xmr_draft,
                                           'orders_dash_draft': orders_dash_draft, 'orders_eth_draft': orders_eth_draft,
                                           'orders_zec_draft': orders_zec_draft, 'orders_btc_draft': orders_btc_draft,
                                           'proffers_ltc_draft': proffers_ltc_draft,
                                           'proffers_xmr_draft': proffers_xmr_draft,
                                           'proffers_dash_draft': proffers_dash_draft,
                                           'proffers_eth_draft': proffers_eth_draft,
                                           'proffers_zec_draft': proffers_zec_draft,
                                           'proffers_btc_draft': proffers_btc_draft,
                                           'user': request.user,
                                           'messages': messages
                                           })


def show_courses(request):
    if not (request.user.is_authenticated()):
        return HttpResponseRedirect('/login/')
    form = AddCourseForm()
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
    courses = CoursesTable(Course.objects.filter(user=request.user))
    return render(request, 'courses.html', {'courses': courses, 'form':form})

def update_courses(request):
    update()
    return HttpResponseRedirect('/login/')

def update_balances():
    conn = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % ('nicechange', 'nicechange'))
    #from eth_rpc_client import Client
    #client = Client(host="127.0.0.1", port="8545")
    for w in Wallet.objects.all():
        w.btcbalance = format(conn.getbalance(w.btcaddress), 'f')
        #w.ethbalance = client.get_balance(w.ethaddress)
        w.save()

def wallets(request):
    #from eth_rpc_client import Client
    #client = Client(host="127.0.0.1", port="8545")
    #balance = client.get_balance("0x6db960f64a986d1c084f8b324e56541b1c541bd3")
    #import web3
    #web3.eth.register("0x6Db960F64A986D1c084F8b324E56541b1c541bD3")
    #web3.eth.Eth.getBalance()
    threading.Thread(target=update_balances).start()
    if not (request.user.is_authenticated()):
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
            pk = sha256(Wallet.objects.count().__str__() + request.user.password)
            pub = privtopub(pk)
            addr = pubtoaddr(pub)
            import sha3
            keccak = sha3.keccak_256()
            keccak.update(pub.encode())
            ethaddr = "0x" + str(keccak.hexdigest()[24:])
            wifKey = encode_privkey(pk, 'wif')
            conn = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % ('nicechange', 'nicechange'))
            conn.importprivkey(wifKey.__str__(), addr.__str__(), False)
            wallet = Wallet(private_key=wifKey, public_key=pub, btcaddress=addr, ethaddress = ethaddr, user=request.user)
            wallet.save()
    wallets = WalletsTable(Wallet.objects.filter(user=request.user))
    return render(request, 'wallets.html', {'wallets': wallets})


def deal(request, thread_id):
    threading.Thread(target=update_balances).start()
    preparehide = 'false'
    givenhide = 'true'
    crsent = 'false'
    from offers.models import TempWallets
    from privatemessages.models import Thread, ThreadActivity
    dealwallet = TempWallets.objects.filter(thread=Thread.objects.filter(id=thread_id).last()).last()
    thread = Thread.objects.filter(id=thread_id).last()
    #conn = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % ('nicechange', 'nicechange'))
    if dealwallet == None:
        pk = sha256(Wallet.objects.count().__str__() + request.user.password+str(random.random()) +
                    TempWallets.objects.count().__str__())
        pub = privtopub(pk)
        addr = pubtoaddr(pub)
        import sha3
        keccak = sha3.keccak_256()
        keccak.update(pub.encode())
        wifKey = encode_privkey(pk, 'wif')
        #conn.importprivkey(wifKey.__str__(), addr.__str__(), False)
        obj = TempWallets.objects.create(thread=Thread.objects.filter(id=thread_id).last(), private_key=wifKey,
                                         public_key=pub, btcaddress=addr)
        obj.save()
        dealwallet = obj
    if  ThreadActivity.objects.filter(user=request.user).last() == None:
        obj = ThreadActivity.objects.create(user=request.user, thread=Thread.objects.filter(id=thread_id).last())
        obj.save()
    else:
        ThreadActivity.objects.filter(user=request.user).last().delete()
        obj = ThreadActivity.objects.create(user=request.user, thread=Thread.objects.filter(id=thread_id).last())
        obj.save()
    wallets = DealWalletsTable(Wallet.objects.filter(user=request.user))
    wallet = DealRole.objects.filter(user=request.user, thread=Thread.objects.filter(id=thread_id).last()).last().wallet
    quantity = str(thread.deal_info).split(' ')[-1]
    if wallet == None:
        wallet = Wallet.objects.filter(user=request.user).last()
        dr = DealRole.objects.filter(user=request.user).last()
        dr.wallet = wallet
        dr.save()
    if DealRole.objects.filter(user=request.user, thread=Thread.objects.filter(id=thread_id).last()).last().role == 'seller':
          buyerwallet = DealRole.objects.filter(role='buyer',
                                                thread=Thread.objects.filter(id=thread_id).last()).last().wallet
          if request.POST:
              if(request.POST.get('prepare')):
                  #if not (conn.getbalance(wallet.btcaddress) < float(float(quantity))):
                      #перевод блокируемой крипты на кошелек биржи
                      #conn.move(wallet.btcaddress, dealwallet.btcaddress, float(float(quantity)))
                      import redis
                      r = redis.StrictRedis()
                      ch = r.pubsub_channels()
                      preparehide = 'true'
                      r.publish("".join(["thread_", thread_id, "_messages"]), '119')
                      r.publish("".join(["thread_", thread_id, "_messages"]), '119')
                      r.publish(77, '119')
                      r.publish(77, '119')
                      r.publish(77, '119')
                      r.publish(77, '119')
                      givenhide = 'false'
              if (request.POST.get('given')):
                #ввод шестизначного кода
                #перевод крипты с кошелька биржи на кошелек адресата
                import redis
                r = redis.StrictRedis()
                ch = r.pubsub_channels()
                r.publish(77, '119')
                #conn.move(dealwallet.btcaddress, buyerwallet.btcaddress, float(float(quantity)))
                crsent = 'true'
              if (request.POST.get('cancel')):
                  #if not (conn.getbalance(dealwallet.btcaddress) == float(float(quantity))):
                      # перевод блокируемой крипты обратно
                      #conn.move(dealwallet.btcaddress, wallet.btcaddress, float(float(quantity)))
                  pass
                  return HttpResponseRedirect('/test/')

          return render(request, 'seller.html', {'wallets': wallets, 'wallet':wallet.btcaddress, 'hide_button_prepare':preparehide,
                                                 'hide_button_given': givenhide, 'id':thread_id, 'crsent':crsent})
    else:
          if request.POST:
              if(request.POST.get('sent')):
                  #списание средств с кошелька биржи, если пришло сообщение "фиат получен" - это узнается у сервера
                  #если сообщения нет - ожидаем
                    pass
              if (request.POST.get('cancel')):
                        return HttpResponseRedirect('/test/')
          return render(request, 'buyer.html', {'wallets': wallets, 'wallet':wallet.btcaddress, 'id':thread_id})



















