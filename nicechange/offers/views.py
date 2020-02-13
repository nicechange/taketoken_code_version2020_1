# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from offers.forms import AddOrderForm, AddOfferForm, AddProfferForm,AddReplyForm, TransactionForm, AddCourseForm, DealForm, DateForm
from django.http import HttpResponseRedirect
from offers.models import Order, Proffer, Course, BurseCourse, Wallet, DealRole, Reply
from offers.tables import MyOrdersTable, MyProffersTable, MyOrdersTableDraft, MyProffersTableDraft, CoursesTable, WalletsTable, DealWalletsTable
from privatemessages.models import Read
from blockchain import wallet
from offers.burses import update
from bitcoin import *
from offers.offerstable import MyRepliesTable, MyFDTable
from accounts.models import Notifications
import socket
import bitcoinrpc
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import threading
from decimal import *
import time
from offers.deals import deal_start_proffer
from offers.models import BurseCourse
from accounts.models import Admins
#from cryptocompy import coin
import requests
#from pycbrf.toolbox import ExchangeRates
from privatemessages.models import Blocked


from templated_email import send_templated_mail
def add_order(request):
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')
    form = AddOrderForm
    user=request.user
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.owner = request.user.username
            order.save()
            users = User.objects.all()
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

def add_proffer(request):
    exists = 'false'
    threading.Thread(target=update).start()
    if not (request.user.is_authenticated):
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
            if not (1 == 4):#(Proffer.objects.filter(user=request.user).exists()):
                proffer = form.save(commit=False)
                proffer.rate = round(float(proffer.rate))
                proffer.user = request.user
                proffer.owner = request.user.username
                proffer.save()
                users = User.objects.all()
                from templated_email import send_templated_mail
                if Notifications.objects.filter(user=request.user, post=True).last():
                    threading.Thread(target=send_templated_mail, args=("putoffer.html", 'from@example.com',
                                                                       [user.email],
                                                                       {
                                                                           'username': user.username,
                                                                           'token': proffer.type_of_token,
                                                                           'rate': proffer.rate
                                                                       }
                                                                       )).start()

                #for user in users:
                    #mailer.send('Уведомление', 'shnicechange@gmail.com')
                return HttpResponseRedirect('/cabinet/')
            else:
                exists = 'true'
    return render(request, 'addproffer.html',  {'form': form, 'course_btc_buy': course_btc_buy, 'course_btc_sale': course_btc_sale,
                                                'course_eth_buy': course_eth_buy,
                                                'course_eth_sale': course_eth_sale,
                                                'course_ltc_buy': course_ltc_buy, 'course_ltc_sale': course_ltc_sale, 'exists':exists})

@login_required(login_url='/login/')
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
    usernm = proffer.user.username
    banks = proffer.bank
    rate = proffer.rate
    user = request.user
    min = proffer.min
    max = proffer.max
    maxbtc = 0
    wlttest = Wallet.objects.filter(user=proffer.user).last()
    conn = AuthServiceProxy("http://%s:%s@188.134.66.68:8332" % ('nicechange', 'nicechange'))
    bln = float(conn.getbalance(wlttest.btcaddress))
    if (bln < round((proffer.max/proffer.rate), 8)) and proffer.type == 'ПРОДАМ':
        return HttpResponseRedirect('/nicechange/forbidden/')
    if proffer.user == request.user:
        return HttpResponseRedirect('/nicechange/own/')
    info = proffer.info
    if info == '':
        info = 'Дополнительная информация'
    if min == 0.0:
        min = '(Нет)'
    if max == 0.0:
        max = '(Нет)'
    if proffer.type == 'КУПЛЮ':
        replytype = 'ПРОДАЖА'
        for wlt in Wallet.objects.filter(user=request.user):
            maxbtc += float(wlt.btcbalance)
    else:
        replytype = 'ПОКУПКА'
        maxbtc = proffer.max/proffer.rate
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.user_to = proffer.user
            proffer = Proffer.objects.get(id=item_id)
            reply.proffer = proffer
            proffer.replies_count = proffer.replies_count + 1
            reply.sellorbuy = replytype
            reply.bank = proffer.bank
            reply.price = float(proffer.rate) * reply.quantity
            reply.quantity = "%f" % (reply.quantity)
            proffer.save()
            reply.save()
            from templated_email import send_templated_mail
            if Notifications.objects.get(user=request.user).reply ==  True:
                threading.Thread(target=send_templated_mail, args=("roffer2.html",
                                                                   'from@example.com',
                                                                   [request.user.email],
                                                                   {
                                                                       'username': request.user.username,
                                                                       'token': proffer.type_of_token,
                                                                       'rate': proffer.rate
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
                        'rate': proffer.rate,
                    },

                )
            if Notifications.objects.get(user=request.user).deal == True:
                send_templated_mail(
                    template_name="start.html",
                    from_email='from@example.com',
                    recipient_list=[proffer.user.email],
                    context={
                        'username': proffer.user.username
                    },

                )

                send_templated_mail(
                    template_name="start.html",
                    from_email='from@example.com',
                    recipient_list=[request.user.email],
                    context={
                        'username': request.user.username
                    },

                )

            return HttpResponseRedirect('/dealstartproffer/'+ str(reply.id))
            deal_start_proffer(request, reply.id)
    return render(request, 'answer.html', {'user_id':user_id, 'form': form, 'id':item_id, 'rate':rate, 'ratestrip':rate,
                                           'replytype':replytype, 'usernm':usernm, 'banks':banks, 'min':min, 'max':max, 'info':info, 'maxbtc':maxbtc})



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
    if not (request.user.is_authenticated):
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
        return HttpResponseRedirect('/broker/')



def user(request):
    if not (request.user.is_authenticated):
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

def my_for_broker(request):
    if not (request.user.is_authenticated):
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



class Answers():
    def __init__(self, row, table):
        self.row = row
        self.table = table


from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from privatemessages.models import Thread
import redis
from online_users.models import OnlineUserActivity
from offers.models import FinishedDeals

def replies(request):
    replies_calc = Reply.objects.filter(user=request.user)
    replies_table = MyRepliesTable(replies_calc)
    finished_deals = MyFDTable(FinishedDeals.objects.filter(user=request.user))
    return render(request, 'replies.html', {'replies_table': replies_table, 'finished_deals':finished_deals })

import datetime
def broker(request, thread_id = None):
    flag_create = 0
    if not request.user.is_authenticated:
        # return HttpResponse("Please sign in.")
        return HttpResponseRedirect('/login/')
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
    finished_deals = FinishedDeals.objects.filter(user=request.user)
    from datetime import timedelta
    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=60))
    active_users = (user for user in user_activity_objects)
    for u in active_users:
        online_users.append(u.user)
    course_btc_sale = 0
    total_summ = 0
    bankrot = 'false'
    wallets = Wallet.objects.filter(user=request.user)
    for w in wallets:
        total_summ += float(w.btcbalance)
    if total_summ == 0:
        bankrot = 'true'
    mode = 'КУПЛЮ'
    display = 'display: none'
    messages = None
    messages_total = None
    messages_sent = None
    messages_received = None
    role = None
    partner = None
    thread = None
    info = None
    warning = None
    if thread_id:
        display = None
        warning = None
        if not request.user.is_authenticated:
            # return HttpResponse("Please sign in.")
            return HttpResponseRedirect('/login/')

        thread = get_object_or_404(
            Thread,
            id=thread_id,
            participants__id=request.user.id
        )
        info = thread.deal_info
        messages = thread.message_set.order_by("datetime")[:100]

        user_id = str(request.user.id)

        r = redis.StrictRedis()

        messages_total = r.hget(
            "".join(["thread_", thread_id, "_messages"]),
            "total_messages"
        )

        messages_sent = r.hget(
            "".join(["thread_", thread_id, "_messages"]),
            "".join(["from_", user_id])
        )

        if messages_total:
            messages_total = int(messages_total)
        else:
            messages_total = 0

        if messages_sent:
            messages_sent = int(messages_sent)
        else:
            messages_sent = 0

        messages_received = messages_total - messages_sent
        partner = thread.participants.exclude(id=request.user.id)[0]

        read = Read.objects.filter(user=user_id, thread=thread).last()
        if read:
            if read.read == False:
                read.read = True
                read.save()

        tz = request.COOKIES.get("timezone")
        if tz:
            timezone.activate(tz)
        if DealRole.objects.filter(user=request.user,
                                   thread=Thread.objects.filter(id=thread_id).last()).last().role == 'seller':
            role = 'Продавец'
        else:
            role = 'Покупатель'
        if request.POST:

            if DealRole.objects.filter(user=request.user,
                                       thread=Thread.objects.filter(id=thread_id).last()).last().role == 'seller':
                warning = True
                quantity = float(str(thread.deal_info).split(' ')[-1])
                wallets = Wallet.objects.filter(user=request.user)
                for wallet in wallets:
                    if not (float(wallet.btcbalance) < quantity):
                        warning = False
                if not warning:
                    return HttpResponseRedirect('/deal/' + thread_id)
            else:
                return HttpResponseRedirect('/deal/' + thread_id)
    if not (request.user.is_authenticated):
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
    user = request.user
    condition = Course.objects.filter(user=request.user, sellorbuy='ПОКУПКА', type_of_token='BTC').last()
    brs = None
    prc = None
    brsbuy = None
    prcsale = None
    brssale = None
    prcbuy = None
    if condition:
        crs = float(BurseCourse.objects.filter(burse=Course.objects.filter(user=request.user,
                                                                               sellorbuy='ПОКУПКА',
                                                                           type_of_token='BTC').last().burse,
                                               token='BTC').last().course)
        brsbuy = Course.objects.filter(user=request.user,
                                    sellorbuy='ПОКУПКА',
                                    type_of_token='BTC').last().burse
        prcbuy = Course.objects.filter(user=request.user,
                                    sellorbuy='ПОКУПКА',
                                    type_of_token='BTC').last().percent
        course_btc_buy = crs - (crs / 100 * condition.percent)
    else:
        course_btc_buy = 0
    condition = Course.objects.filter(user=request.user, sellorbuy='ПРОДАЖА', type_of_token='BTC').last()
    if condition:
        crs = float(BurseCourse.objects.filter(burse=Course.objects.filter(user=request.user,
                                                                           sellorbuy='ПРОДАЖА',
                                                                           type_of_token='BTC').last().burse,
                                               token='BTC').last().course)
        brssale = Course.objects.filter(user=request.user,
                                    sellorbuy='ПРОДАЖА',
                                    type_of_token='BTC').last().burse
        prcsale = Course.objects.filter(user=request.user,
                                    sellorbuy='ПРОДАЖА',
                                    type_of_token='BTC').last().percent
        course_btc_sale = crs + (crs / 100 * condition.percent)
    course_btc_buy = int(round(course_btc_buy))
    course_btc_sale = int(round(course_btc_sale))
    sum = 0
    answr = 0
    answr = Reply.objects.filter(user_to=request.user).count()
    for wlt in Wallet.objects.filter(user=request.user):
        sum += float(wlt.btcbalance)
    totalbtc = sum
    read = True
    for th in threads:
        if th.read == False:
            read = False
    if not read:
        messages_flag = 'Есть непрочитанные.'
    else:
        messages_flag = 'Непрочитанных нет.'

    form = AddProfferForm()
    answers_list = []
    lim = total_summ * course_btc_sale
    dealings_sum = 0
    proffers_publicate = Proffer.objects.filter(user=request.user, state='Published')
    for pr in proffers_publicate:
        dealings_sum += pr.max
    max_limit = int(lim - dealings_sum)
    for proffer in Proffer.objects.filter(type_of_token__contains="BTC", user=request.user).exclude(state="Draft"):
        replys = MyRepliesTable(Reply.objects.filter(proffer=proffer))
        for ans in Reply.objects.filter(proffer=proffer):
            if ans.time < finishdate.time():
                proffer = ans.proffer
                proffer.replies_count = proffer.replies_count - 1
                proffer.save()
                if ans.thread:
                    thread = Thread.objects.filter(id=ans.thread.id)
                    thread.delete()
                ans.delete()
        if Reply.objects.filter(proffer=proffer).count() == 0:
            replys = None
        ans = Answers(proffer, replys)
        answers_list.append(ans)
    if request.method == 'POST':
        form = AddProfferForm(request.POST)
        if form.is_valid():
            if 'buybutton' in form.data:
                mode = 'КУПЛЮ'
                brs = brsbuy
                prc = prcbuy
            if 'salebutton' in form.data:
                mode = 'ПРОДАМ'
                brs = brssale
                prc = prcsale
            if not (1 == 4):#(Proffer.objects.filter(user=request.user).exists()):
                banks = ''
                proffer = form.save(commit=False)
                proffer.rate = round(float(proffer.rate))
                proffer.user = request.user
                proffer.owner = request.user.username
                proffer.type_of_token = 'BTC'
                proffer.type = mode
                if form.cleaned_data['bank_sber'] == True:
                    banks = 'Сбербанк'
                if form.cleaned_data['bank_promsvyaz'] == True:
                        banks = banks + ', Промсвязьбанк'
                if form.cleaned_data['bank_vtb'] == True:
                        banks = banks + ', Втб-24'
                if form.cleaned_data['bank_qiwi'] == True:
                        banks = banks + ', QIWI'
                if form.cleaned_data['bank_tinkoff'] == True:
                        banks = banks + ', Тинькофф'
                if form.cleaned_data['bank_alfa'] == True:
                    banks = banks + ', Альфабанк'
                if form.cleaned_data['bank_yandex'] == True:
                        banks = banks + ', Яндекс.Деньги'
                proffer.bank = banks
                if form.cleaned_data['min'] > form.cleaned_data['max']:
                    proffer.limit = str(form.cleaned_data['max']) + " - " + str(form.cleaned_data['min']) + " RUB"
                else:
                    proffer.limit = str(form.cleaned_data['min'])+ " - "+ str(form.cleaned_data['max'])+" RUB"
                sum = 0
                for wlt in Wallet.objects.filter(user=request.user):
                    sum += float(wlt.btcbalance)
                proffer.prc = prc
                proffer.brs = brs
                proffer.balance = sum*proffer.rate
                proffer.profile_id = proffer.user_id
                proffer.save()
                flag_create = 1
                if proffer.min > proffer.max:
                    proffer.min, proffer.max = proffer.max, proffer.min
                    proffer.save()

                users = User.objects.all()
                from templated_email import send_templated_mail
                if Notifications.objects.get(user=request.user).post == True:
                    threading.Thread(target=send_templated_mail, args=("putoffer.html", 'from@example.com',
                                                                       [user.email],
                                                                       {
                                                                           'username': user.username,
                                                                           'token': proffer.type_of_token,
                                                                           'rate': proffer.rate
                                                                       }
                                                                       )).start()

    return render(request, 'dealings_new.html', {'orders_ltc': orders_ltc, 'orders_xmr': orders_xmr,
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
                                           'messages_flag': messages_flag,
                                             "thread_id": thread_id,
                                             "thread_messages": messages,
                                             "messages_total": messages_total,
                                             "messages_sent": messages_sent,
                                             "messages_received": messages_received,
                                             "partner": partner,
                                             "deal_info": info,
                                             "warning": warning,
                                              "display": display,
                                                 "user_to":partner,
                                                 "role":role,
                                                 "mode":mode,
                                                 "form":form,
                                                 'course_btc_buy': course_btc_buy,
                                                 'course_btc_sale': course_btc_sale,
                                                 'answers': answers_list,
                                                 'online_users':online_users,
                                                 'finiched_deals':finished_deals,
                                                 'max_limit': max_limit,
                                                 'bankrot': bankrot,
                                                 'totalbtc': totalbtc,
                                                 'answr':answr,
                                                 'totalsumm':total_summ,
                                                 'flag':flag_create
                                           })


def show_courses(request):
    threading.Thread(target=update).start()
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')
    form = AddCourseForm()
    valid = ''
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            for crs in Course.objects.filter(user=request.user, sellorbuy=course.sellorbuy,
                                             type_of_token=course.type_of_token).all():
                      crs.delete()
            course.save()
    courses = CoursesTable(Course.objects.filter(user=request.user))
    return render(request, 'rates.html', {'courses': courses, 'form':form, 'valid':valid})


def update_courses(request):
    update()
    return HttpResponseRedirect('/login/')

def update_balances():
    conn = AuthServiceProxy("http://%s:%s@188.134.66.68:8332" % ('nicechange', 'nicechange'))
    #from eth_rpc_client import Client
    #client = Client(host="127.0.0.1", port="8545")
    for w in Wallet.objects.all():
        w.btcbalance = format(conn.getbalance(w.btcaddress), 'f')
        #w.ethbalance = client.get_balance(w.ethaddress)
        w.save()

def wallets(request):
    dateform = DateForm()
    if not request.user.is_authenticated:
        # return HttpResponse("Please sign in.")
        return HttpResponseRedirect('/login/')
    #from eth_rpc_client import Client
    #client = Client(host="127.0.0.1", port="8545")
    #balance = client.get_balance("0x6db960f64a986d1c084f8b324e56541b1c541bd3")
    #import web3
    #web3.eth.register("0x6Db960F64A986D1c084F8b324E56541b1c541bD3")
    #web3.eth.Eth.getBalance()
    threading.Thread(target=update_balances).start()
    blocked = 0
    fee = 0
    final = 0
    for w in Wallet.objects.filter(user=request.user):
        final = final + float(w.btcbalance)
    fixfinal = final
    b = Blocked.objects.filter(user=request.user).last()
    if b:
        if b.blocked:
            blocked = "%f" % (b.blocked)
        if b.fee:
            fee = "%f" % (b.fee)
        if b.real != None:
            final = "%f" % (b.real)
        if fee == blocked == 0:
            final = fixfinal
            b.real = final
            b.save()
    else:
        final =  "%f" % (final)

    conn = AuthServiceProxy("http://%s:%s@188.134.66.68:8332" % ('nicechange', 'nicechange'))
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')
    if Wallet.objects.filter(user=request.user).count() == 0:
            pk = sha256(Wallet.objects.count().__str__() + request.user.password + 'Taketoken')
            pub = privtopub(pk)
            addr = pubtoaddr(pub)
            import sha3
            keccak = sha3.keccak_256()
            keccak.update(pub.encode())
            ethaddr = "0x" + str(keccak.hexdigest()[24:])
            wifKey = encode_privkey(pk, 'wif')
            conn.importprivkey(wifKey.__str__(), addr.__str__(), False)
            wallet = Wallet(private_key=wifKey, public_key=pub, btcaddress=addr, ethaddress = ethaddr, user=request.user)
            wallet.save()

    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)
    addr = Wallet.objects.filter(user=request.user).last().btcaddress
    #addr = '17YiuD2sHUaz351cDr3HomtSWFF5sWfyUa' #todel
    date1 = date2 = None
    if request.method == 'POST':
        dateform = DateForm(request.POST)
        if dateform.is_valid():
            if dateform.cleaned_data['date1'] and dateform.cleaned_data['date2']:
                date1 = dateform.cleaned_data['date1']
                date2 = dateform.cleaned_data['date2']
    info_dict = conn.listtransactions(addr)
    r_info_dict = []
    for el in info_dict:
        from datetime import datetime
        el['time'] = datetime.fromtimestamp(el['time'])
        el = Struct(**el)
        if date1 and date2:
            if not (el.time.date() < date1 or el.time.date() > date2):
                r_info_dict.append(el)
        else:
            r_info_dict.append(el)
    info = r_info_dict
    wallets = WalletsTable(Wallet.objects.filter(user=request.user))
    return render(request, 'wallets.html', {'dateform':dateform, 'wallets': wallets, 'user':request.user, 'blocked':blocked, 'final':final, 'fee':fee,  'addr' :addr, 'info' : info})

def deal(request, thread_id):
    is_seller = 'false'
    import datetime
    import pytz
    try:
        thread = Thread.objects.get(id=thread_id)
    except:
        return render(request, 'pasterror.html')
    reply = Reply.objects.get(thread=thread)
    watch = reply
    time = reply.time
    quantity = reply.quantity
    price = reply.quantity * Proffer.objects.get(id=reply.proffer_id).rate
    codemsg = ''
    verif = False
    ans = reply
    if ans.trying == True and ans.confirm == True:
        codemsg = 'Код верифицирован.'
        verif = True
    if ans.trying == True and ans.confirm == False:
        codemsg = 'Код не верен.'
    buyerwallet = None
    partner = None
    if reply.sellorbuy == "ПРОДАЖА":
        seller = User.objects.get(id=reply.user_id).username
        wts = Wallet.objects.filter(user=reply.user_id)
        wallet = wts.last()
        for w in wts:
            if w.btcbalance > wallet.btcbalance:
                wallet = w
        buyer = User.objects.get(id=reply.user_to_id).username
        buyerwallet = Wallet.objects.filter(user=reply.user_to_id).last()
        sellerid = reply.user_id
    else:
        seller = User.objects.get(id=reply.user_to_id).username
        wts = Wallet.objects.filter(user=reply.user_to_id)
        wallet = wts.last()
        for w in wts:
            if w.btcbalance > wallet.btcbalance:
                wallet = w
        buyer = User.objects.get(id=reply.user_id).username
        buyerwallet = Wallet.objects.filter(user=reply.user_id).last()
        sellerid = reply.user_to_id
    if request.user != User.objects.get(id=reply.user_to_id):
        partner = User.objects.get(id=reply.user_to_id)
    else:
        partner = reply.user
    if request.user.id == sellerid:
        is_seller = 'true'
    timestart_h = time.hour
    timestart_m = time.minute
    timestart_s = time.second
    date_y = reply.date.year
    date_m = reply.date.month
    date_d = reply.date.day

    display = 'display: none'
    messages = None
    messages_total = None
    messages_sent = None
    messages_received = None
    role = None
    mess = ''

    info = None
    warning = None
    if thread_id:
        display = None
        warning = None
        if not request.user.is_authenticated:
            # return HttpResponse("Please sign in.")
            return HttpResponseRedirect('/login/')


        info = thread.deal_info
        messages = thread.message_set.order_by("datetime")[:100]

        user_id = str(request.user.id)

        r = redis.StrictRedis()

        messages_total = r.hget(
            "".join(["thread_", thread_id, "_messages"]),
            "total_messages"
        )

        messages_sent = r.hget(
            "".join(["thread_", thread_id, "_messages"]),
            "".join(["from_", user_id])
        )

        if messages_total:
            messages_total = int(messages_total)
        else:
            messages_total = 0

        if messages_sent:
            messages_sent = int(messages_sent)
        else:
            messages_sent = 0

        messages_received = messages_total - messages_sent

        read = Read.objects.filter(user=user_id, thread=thread).last()
        if read:
            if read.read == False:
                read.read = True
                read.save()

        tz = request.COOKIES.get("timezone")
        if tz:
            timezone.activate(tz)
    # threading.Thread(target=update_balances).start()
    # preparehide = 'false'
    # givenhide = 'true'
    # crsent = 'false'
    from offers.models import TempWallets
    from privatemessages.models import ThreadActivity
    dealwallet = TempWallets.objects.filter(thread=Thread.objects.filter(id=thread_id).last()).last()
    thread = Thread.objects.filter(id=thread_id).last()
    conn = AuthServiceProxy("http://%s:%s@188.134.66.68:8332" % ('nicechange', 'nicechange'))

    if dealwallet == None:
        pk = sha256(Wallet.objects.count().__str__() + request.user.password+str(random.random()) +
                    TempWallets.objects.count().__str__())
        pub = privtopub(pk)
        addr = pubtoaddr(pub)
        import sha3
        keccak = sha3.keccak_256()
        keccak.update(pub.encode())
        wifKey = encode_privkey(pk, 'wif')
        conn.importprivkey(wifKey.__str__(  ), addr.__str__(), False)
        obj = TempWallets.objects.create(thread=Thread.objects.filter(id=thread_id).last(), private_key=wifKey,
                                         public_key=pub, btcaddress=addr)
        obj.save()
        dealwallet = obj
    # if  ThreadActivity.objects.filter(user=request.user).last() == None:
    #     obj = ThreadActivity.objects.create(user=request.user, thread=Thread.objects.filter(id=thread_id).last())
    #     obj.save()
    # else:
    #     ThreadActivity.objects.filter(user=request.user).last().delete()
    #     obj = ThreadActivity.objects.create(user=request.user, thread=Thread.objects.filter(id=thread_id).last())
    #     obj.save()
    # wallets = DealWalletsTable(Wallet.objects.filter(user=request.user))
    # wallet = DealRole.objects.filter(user=request.user, thread=Thread.objects.filter(id=thread_id).last()).last().wallet
    # quantity = str(thread.deal_info).split(' ')[-1]
    # fiat = str(thread.deal_info).split(' ')[-3]
    # if wallet == None:
    #     wallet = Wallet.objects.filter(user=request.user).last()
    #     dr = DealRole.objects.filter(user=request.user, thread=Thread.objects.filter(id=thread_id).last()).last()
    #     dr.wallet = wallet
    #     dr.save()
    # if DealRole.objects.filter(user=request.user, thread=Thread.objects.filter(id=thread_id).last()).last().role == 'seller':
    #       buyerwallet = DealRole.objects.filter(role='buyer',
    #                                             thread=Thread.objects.filter(id=thread_id).last()).last().wallet
    #       partner = buyerwallet.user
    #       sellerbalance = wallet.btcbalance
    userbl = User.objects.get(id=sellerid)
    bl = Blocked.objects.filter(user=userbl).last()
    admi = Admins.objects.all().last()
    if admi != None:
        per = round(float(quantity), 8) / 100 * float(admi.percent)
    bal = float(conn.getbalance(wallet.btcaddress))
    if not bl:
        bl = Blocked.objects.create(user=userbl)
    if (not (bal) < float(quantity)) and not(conn.getbalance(dealwallet.btcaddress) > 0 ):
          #перевод блокируемой крипты на кошелек биржи
          thread.twallet = dealwallet.btcaddress
          thread.destwallet = wallet.btcaddress
          thread.quantity = float(quantity + per)
          thread.bl = bl
          thread.save()
          bl.real = bal
          SUMMA = float(quantity + per)
          conn.move(wallet.btcaddress, dealwallet.btcaddress, round(SUMMA, 8))
          bl.fee = per
          bl.blocked = round(float(quantity), 8)
          bl.save()
    #           if ('given' in request.POST):
    #             #ввод шестизначного кода (не сделан)
    #             #перевод крипты с кошелька биржи на кошелек адресата
    #             conn.move(dealwallet.btcaddress, buyerwallet.btcaddress, round(float(quantity), 8))
    #             crsent = 'true'
    #             preparehide = 'true'
    #             givenhide = 'true'
    #             # сделка добавляется в таблицу со статусом завершена
    #             fd = FinishedDeals(user=request.user, partner=partner.username, price=fiat, status="Завершена")
    #             fd.save()
    #             fd = FinishedDeals(user=partner, partner=request.user.username, price=fiat, status="Завершена")
    #             fd.save()
    #           if ('cancel' in request.POST):
    #               if (round(float(conn.getbalance(dealwallet.btcaddress)), 8)) == round(float(quantity), 8):
    #                   # перевод блокируемой крипты обратно
    #                   # сделка добавляется в таблицу со статусом отмены
    #                   fd = FinishedDeals(user=request.user, partner=partner.username, price=fiat, status="Отменена")
    #                   fd.save()
    #                   fd = FinishedDeals(user=partner, partner=request.user.username, price=fiat, status="Отменена")
    #                   fd.save()
    #                   conn.move(dealwallet.btcaddress, wallet.btcaddress, round(float(quantity), 8))
    #                   return HttpResponseRedirect('/test/')
    #
    #       return render(request, 'seller.html', {'wallets': wallets, 'wallet':wallet.btcaddress, 'hide_button_prepare':preparehide,
    #                                              'hide_button_given': givenhide, 'id':thread_id, 'crsent':crsent
    #                                               ,'sellerbalance':sellerbalance, 'quantity':quantity})
    # else:
    #       if request.POST:
    #           if('sent' in request.POST):
    #               #списание средств с кошелька биржи, если пришло сообщение "фиат получен" - это узнается у сервера
    #               #если сообщения нет - ожидаем
    #                 pass
    #           if ('cancel' in request.POST):
    #                       sellerwallet = DealRole.objects.filter(role='seller',
    #                                                             thread=Thread.objects.filter(id=thread_id).last()).last().wallet
    #                       fd = FinishedDeals(user=request.user, partner=sellerwallet.user.username, price=fiat, status="Отменена")
    #                       fd.save()
    #                       return HttpResponseRedirect('/test/')
    dealq = None
    fiat = price.__str__()
    mess = codemsg
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            if 'cancel' in form.data:
              dealq = 'cancel' #перевод средств с пром. кошелька на кошелек продавца
              if ('cancel' in request.POST):
                      # перевод блокируемой крипты обратно
                      # сделка добавляется в таблицу со статусом отмены
                      answer = Reply.objects.get(thread=thread)
                      proffer = answer.proffer
                      fd = FinishedDeals(user=request.user, bank=proffer.bank, partner=partner.username, quantity=quantity, price=fiat, status="Отменена")
                      fd.save()
                      fd = FinishedDeals(user=partner, bank=proffer.bank, partner=request.user.username, quantity=quantity, price=fiat, status="Отменена")
                      fd.save()
                      conn.move(dealwallet.btcaddress, wallet.btcaddress, float(quantity + per))
                      proffer.replies_count = proffer.replies_count - 1
                      proffer.save()
                      answer.delete()
                      thread.delete()
                      bls = Blocked.objects.filter(user=sellerid).last()
                      bls.fee = bls.fee - per
                      bls.blocked = bls.blocked - round(float(quantity), 8)
                      bls.save()
                      if Notifications.objects.get(user=request.user).support == True:
                          send_templated_mail(
                              template_name="cancelled.html",
                              from_email='from@example.com',
                              recipient_list=[proffer.user.email],
                              context={
                                  'username': proffer.user.username
                              },

                          )
                      if Notifications.objects.get(user=reply.user).support == True:
                                send_templated_mail(
                                      template_name="cancelled.html",
                                      from_email='from@example.com',
                                      recipient_list=[reply.user.email],
                                      context={
                                          'username': reply.user.username
                                      },

                                  )
            if 'fiat' in form.data:
                if verif == True:
                    admi = Admins.objects.all().last()
                    dealq = 'fiat' #перевод средств с пром.кошелька на кошелек покупателя
                    per = round(float(quantity), 8)/100 * float(admi.percent)
                    summ = round(float(quantity), 8)
                    admi.sum = float(admi.sum) + summ
                    admi.walletsum = float(admi.walletsum) + per
                    admi.count = int(admi.count) + 1
                    admi.save()
                    conn.move(dealwallet.btcaddress, buyerwallet.btcaddress, summ)
                    conn.move(dealwallet.btcaddress, admi.address, round(per, 8))
                    # сделка добавляется в таблицу со статусом завершена
                    answer = Reply.objects.get(thread=thread)
                    proffer = answer.proffer
                    fd = FinishedDeals.objects.create(user=request.user, bank=proffer.bank, quantity=quantity, partner=partner.username, price=fiat, status="Завершена")
                    fd.save()
                    fd = FinishedDeals.objects.create(user=partner, bank=proffer.bank, quantity=quantity, partner=request.user.username, price=fiat, status="Завершена")
                    fd.save()
                    proffer.user.profile.dealscount = proffer.user.profile.dealscount + 1
                    answer.user.profile.dealscount = answer.user.profile.dealscount + 1
                    olddeals = FinishedDeals.objects.filter(user=proffer.user)
                    partners = []
                    for od in olddeals:
                        partners.append(od.partner)
                    if not (answer.user in partners):
                        proffer.user.profile.uniquedealscount = proffer.user.profile.uniquedealscount + 1
                    proffer.user.profile.dealscounttext = proffer.user.profile.dealscount
                    if proffer.user.profile.dealscount > 10:
                        proffer.user.profile.dealscounttext = '10+'
                    if proffer.user.profile.dealscount > 100:
                        proffer.user.profile.dealscounttext = '100+'
                    olddeals = FinishedDeals.objects.filter(user=answer.user)
                    partners = []
                    for od in olddeals:
                        partners.append(od.partner)
                    if not (proffer.user.username in partners):
                        answer.user.profile.uniquedealscount = answer.user.profile.uniquedealscount + 1
                    answer.user.profile.dealscounttext = answer.user.profile.dealscount
                    if answer.user.profile.dealscount > 10:
                        answer.user.profile.dealscounttext = '10+'
                    if answer.user.profile.dealscount > 100:
                        answer.user.profile.dealscounttext = '100+'
                    proffer.replies_count = proffer.replies_count - 1
                    proffer.save()
                    proffer.user.profile.save()
                    answer.user.profile.save()
                    answer.delete()
                    thread.delete()
                    bls = Blocked.objects.filter(user=sellerid).last()
                    bls.fee = bls.fee - per
                    bls.real = bls.real - bls.blocked - per
                    bls.blocked = bls.blocked - round(float(quantity), 8)
                    bls.save()
                    if Notifications.objects.get(user=request.user).support == True:
                        send_templated_mail(
                            template_name="finished.html",
                            from_email='from@example.com',
                            recipient_list=[proffer.user.email],
                            context={
                                'username': proffer.user.username
                            },

                        )
                    if Notifications.objects.get(user=reply.user).support == True:
                            send_templated_mail(
                                template_name="finished.html",
                                from_email='from@example.com',
                                recipient_list=[reply.user.email],
                                context={
                                    'username': reply.user.username
                                },

                            )
                else:
                    return HttpResponseRedirect('/codeauth2/' + str(reply.id))
    return render(request, 'smartdeal.html', {'timestart':time, 'seller':seller, 'buyer':buyer, 'quantity':"%f" % (quantity), 'price':price, 'watch':watch,
                                              'timestart_h':timestart_h, 'timestart_m':timestart_m, 'timestart_s':timestart_s,
                                              'date_d':date_d, 'date_m':date_m, 'date_y':date_y, "thread_id": thread_id,
                                             "thread_messages": messages,
                                             "messages_total": messages_total,
                                             "messages_sent": messages_sent,
                                             "messages_received": messages_received,
                                             "partner": partner,
                                             "deal_info": info,
                                             "warning": warning,
                                              "display": display,
                                              "is_seller":is_seller,
                                              "dealq":dealq,
                                              "mess":mess,
                                              "DealForm": DealForm})



@login_required(login_url='/login/')
def delete_deal(request, item_id):
    # conn = AuthServiceProxy("http://%s:%s@195.131.139.14:8332" % ('nicechange', 'nicechange'))
    #thread = Thread.objects.filter(id=item_id).last()
    # bl = thread.bl
    # bl.blocked = 0
    # bl.fee = 0
    # bl.save()
    # conn.move(thread.twallet, thread.destwallet, thread.quantity)
    # answer = Reply.objects.get(thread=thread)
    # proffer = answer.proffer
    # proffer.replies_count = proffer.replies_count - 1
    # proffer.save()
    # answer.delete()
    # thread.delete()
    return HttpResponseRedirect('/wallets/')

@login_required(login_url='/login/')
def delete_fdeal(request, item_id):
    deal = FinishedDeals.objects.get(id=item_id)
    deal.delete()
    return HttpResponseRedirect('/replies/')

from offers.forms import PromoUserForm
def promo(request):
    form = PromoUserForm()
    msg = ""
    if request.method == 'POST':
        form = PromoUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] == 1:
                return HttpResponseRedirect('/nicechange/')
            else:
                msg = 'Неверный код'
        else:
                return render(request, 'registration/login_err.html')
    return render(request, 'promo.html', {"form":form, "msg":msg})











