# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from offers.models import Offer, Reply, DealRole
from privatemessages.models import Thread
from django.http import HttpResponseRedirect
from accounts.models import Notifications
import threading

@login_required
def deal_start_order(request, item_id):
    offer = Offer.objects.get(id=item_id)
    user = offer.user
    thread = Thread.objects.create()
    order = offer.order
    thread.deal_info = "Ордер: тип валюты: "+order.offer_type+" количество: "+ order.quantity.__str__()+" банк: "+order.bank+" операция: "+order.sellorbuy
    thread.save()
    partner = request.user
    partner_username = partner.username
    thread.participants.add(request.user, user)
    link = '/broker/' + thread.id.__str__() + '/'
    text = "Привет!"
    from templated_email import send_templated_mail
    threading.Thread(target=send_templated_mail, args=("chat.html",
                                    'from@example.com',
                                    [user.email],
                                    {
                                        'username': user.username,
                                        'partner': partner_username,
                                        'info': thread.deal_info,
                                        'link': link
                                    }
                                    )).start()

    return HttpResponseRedirect(link)


@login_required
def deal_start_proffer(request, item_id):
    reply = Reply.objects.get(id=item_id)
    user = reply.user_to
    if reply.thread:
        if not request.user in reply.thread.participants.all():
            reply.thread.participants.add(request.user)
        link = '/deal/' + reply.thread.id.__str__() + '/'
        return HttpResponseRedirect(link)
    thread = Thread.objects.create()
    proffer = reply.proffer
    thread.deal_info = "Предложение: тип валюты: "+proffer.type_of_token+" курс: "+ proffer.rate.__str__() + " количество: " + reply.quantity.__str__()
    reply.thread = thread
    reply.save()
    thread.save()
    thread.participants.add(request.user, user)#нельзя ответить на свое предложение - будет ошибка
    link = '/deal/' + thread.id.__str__() + '/'
    if reply.sellorbuy == "ПРОДАЖА":
        myrole = 'buyer'
        hisrole = 'seller'
    else:
        myrole = 'seller'
        hisrole = 'buyer'
    obj = DealRole.objects.create(user=request.user, thread=thread, role=myrole, wallet=None)
    obj.save()
    obj = DealRole.objects.create(user=user, thread=thread, role=hisrole, wallet=None)
    obj.save()
    text = "Привет!"
    partner = request.user
    partner_username = partner.username
    from templated_email import send_templated_mail
    if Notifications.objects.get(user=request.user).chat == True:
        send_templated_mail(
                template_name="chat.html",
                from_email='from@example.com',
                recipient_list=[user.email],
                context={
                    'username': user.username,
                    'partner': partner_username,
                    'info':thread.deal_info,
                    'link': link
                },

            )

    return HttpResponseRedirect(link)