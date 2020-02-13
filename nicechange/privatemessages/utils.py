import json

import redis
from django.http import HttpResponse
from django.utils import dateformat
from privatemessages.models import Thread, Read, Blocked
from django.contrib.auth.models import User
from templated_email import send_templated_mail
from django.shortcuts import render, get_object_or_404

from privatemessages.models import Message

def json_response(obj):
    """
    This function takes a Python object (a dictionary or a list)
    as an argument and returns an HttpResponse object containing
    the data from the object exported into the JSON format.
    """
    return HttpResponse(json.dumps(obj), content_type="application/json")

def send_message(thread_id,
                 sender_id,
                 message_text,
                 sender_name=None):
    """
    This function takes Thread object id (first argument),
    sender id (second argument), message text (third argument)
    and can also take sender's name.

    It creates a new Message object and increases the
    values stored in Redis that represent the total number
    of messages for the thread and the number of this thread's
    messages sent from this specific user.

    If a sender's name is passed, it also publishes
    the message in the thread's channel in Redis
    (otherwise it is assumed that the message was
    already published in the channel).
    """

    message = Message()
    message.text = message_text
    message.thread_id = thread_id
    message.sender_id = sender_id
    message.save()
    if message_text == 'Средства отправлены':
        thread = Thread.objects.get(id=thread_id)
        blocked = Blocked.objects.get(id=thread.bl_id)
        user = User.objects.get(id=blocked.user_id)
        send_templated_mail(
            template_name="sended.html",
            from_email='from@example.com',
            recipient_list=[user.email],
            context={
                'username': user.username
            },

        )
    thread_id = str(thread_id)
    sender_id = str(sender_id)

    r = redis.StrictRedis()
    if sender_name:
        r.publish("".join(["thread_", thread_id, "_messages"]), json.dumps({
            "sender": sender_name,
            "timestamp": dateformat.format(message.datetime, 'U'),
            "text": message_text,
        }))

    for key in ("total_messages", "".join(["from_", sender_id])):
        r.hincrby(
            "".join(["thread_", thread_id, "_messages"]),
            key,
            1
        )