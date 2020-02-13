# -*- coding: utf-8 -*-
from django.conf.urls import url
from privatemessages.views import send_message_view, send_message_api_view, messages_view
import privatemessages

urlpatterns = [
    url(r'^send_message/$', send_message_view),
    url(r'^send_message_api/(?P<thread_id>\d+)/$', send_message_api_view),
    url(r'^chat/(?P<thread_id>\d+)/$', privatemessages.views.chat_view, name="privatemessages.views.chat_view"),
    url(r'^$', messages_view),
]
