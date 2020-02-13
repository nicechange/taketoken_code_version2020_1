# Create your views here.

import redis

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.contrib.auth.models import User

from privatemessages.models import Thread, Message, Read

from privatemessages.utils import json_response, send_message

def send_message_view(request):
    if not request.method == "POST":
        return HttpResponse("Please use POST.")

    if not request.user.is_authenticated:
        #return HttpResponse("Please sign in.")
        return HttpResponseRedirect('/login/')

    message_text = request.POST.get("message")

    if not message_text:
        return HttpResponse("No message found.")

    if len(message_text) > 10000:
        return HttpResponse("The message is too long.")

    recipient_name = request.POST.get("recipient_name")

    try:
        recipient = User.objects.get(username=recipient_name)
    except User.DoesNotExist:
        return HttpResponse("No such user.")

    if recipient == request.user:
        return HttpResponse("You cannot send messages to yourself.")

    thread_queryset = Thread.objects.filter(
        participants=recipient
    ).filter(
        participants=request.user
    )

    if thread_queryset.exists():
        thread = thread_queryset[0]
    else:
        thread = Thread.objects.create()
        thread.participants.add(request.user, recipient)

    send_message(
                    thread.id,
                    request.user.id,
                    message_text,
                    request.user.username
                )

    return HttpResponseRedirect(
        '/messages/'
    )

@csrf_exempt
def send_message_api_view(request, thread_id):
    if not request.method == "POST":
        return json_response({"error": "Please use POST."})

    api_key = request.POST.get("api_key")

    if api_key != settings.API_KEY:
        return json_response({"error": "Please pass a correct API key."})

    try:
        thread = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        return json_response({"error": "No such thread."})

    try:
        sender = User.objects.get(id=request.POST.get("sender_id"))
    except User.DoesNotExist:
        return json_response({"error": "No such user."})

    message_text = request.POST.get("message")

    if not message_text:
        return json_response({"error": "No message found."})

    if len(message_text) > 10000:
        return json_response({"error": "The message is too long."})
    print('flag!!!!!');
    send_message(
                    thread.id,
                    sender.id,
                    message_text
                )

    return json_response({"status": "ok"})

def messages_view(request):
    if not request.user.is_authenticated:
        #return HttpResponse("Please sign in.")
        return HttpResponseRedirect('/login/')

    threads = Thread.objects.filter(
        participants=request.user
    ).order_byorder_by("-last_message")

    if not threads:
        return render(request, 'private_messages.html',
                                  {})

    r = redis.StrictRedis()

    user_id = str(request.user.id)

    for thread in threads:
        thread.partner = thread.participants.exclude(id=request.user.id)[0]

        thread.total_messages = r.hget(
            "".join(["thread_", str(thread.id), "_messages"]),
            "total_messages"
        )

    return render(request, 'private_messages.html',
                              {
                                  "threads": threads,
                              })


from offers.models import DealRole
from offers.models import Wallet
def chat_view(request, thread_id):
    warning = None
    if not request.user.is_authenticated:
        #return HttpResponse("Please sign in.")
        return HttpResponseRedirect('/login/')

    thread = get_object_or_404(
        Thread,
        id=thread_id,
        participants__id=request.user.id
    )

    messages = thread.message_set.order_by("-datetime")[:100]

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

    messages_received = messages_total-messages_sent
    partner = thread.participants.exclude(id=request.user.id)[0]

    read = Read.objects.filter(user=user_id, thread=thread).last()
    if read:
        if read.read == False:
            read.read = True
            read.save()

    tz = request.COOKIES.get("timezone")
    if tz:
        timezone.activate(tz)
    if request.POST:
        if DealRole.objects.filter(user=request.user,
                                   thread=Thread.objects.filter(id=thread_id).last()).last().role == 'seller':
            warning = True
            quantity = float(str(thread.deal_info).split(' ')[-1])
            wallets = Wallet.objects.filter(user=request.user)
            for wallet in wallets:
                if not(float(wallet.btcbalance) < quantity):
                    warning = False
            if not warning:
                return HttpResponseRedirect('/deal/' + thread_id)
        else:
            return HttpResponseRedirect('/deal/' + thread_id)
    return render(request, 'chat.html',
                              {
                                  "thread_id": thread_id,
                                  "thread_messages": messages,
                                  "messages_total": messages_total,
                                  "messages_sent": messages_sent,
                                  "messages_received": messages_received,
                                  "partner": partner,
                                  "deal_info": thread.deal_info,
                                  "warning": warning
                              })

