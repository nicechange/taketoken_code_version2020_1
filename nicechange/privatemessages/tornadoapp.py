# -*- coding: utf-8 -*-
import datetime
import json
import time
import urllib

#import brukva
#import aioredis
import tornadoredis
#from aredis import StrictRedis
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpclient
from django.shortcuts import render, get_object_or_404
from privatemessages.models import Read


from django.conf import settings
from importlib import import_module

session_engine = import_module(settings.SESSION_ENGINE)

from django.contrib.auth.models import User

from privatemessages.models import Thread

c = tornadoredis.Client()
c.connect()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write('Hello. :)')

class MessagesHandler(tornado.websocket.WebSocketHandler):

    waiters = set()

    def __init__(self, *args, **kwargs):
        super(MessagesHandler, self).__init__(*args, **kwargs)
        self.client = tornadoredis.Client()
        self.client.connect()

    def check_origin(self, origin):
        return True

    def open(self, thread_id):
        session_key = self.get_cookie(settings.SESSION_COOKIE_NAME)
        session = session_engine.SessionStore(session_key)
        try:
            self.user_id = session["_auth_user_id"]
            self.sender_name = User.objects.get(id=self.user_id).username
        except (KeyError, User.DoesNotExist):
            self.close()
            return
        if not Thread.objects.filter(
            id=thread_id,
            participants__id=self.user_id
        ).exists():
            self.close()
            return
        self.channel = "".join(['thread_', thread_id,'_messages'])
        self.waiters.add((self.channel, self))
        #self.client.subscribe(self.channel)
        self.thread_id = thread_id
        self.client.listen(self.show_new_message)

    def handle_request(self, response):
        pass
# python manage.py starttornadoapp
    def on_message(self, message):
        #f = open('/home/django/filemy.txt', 'a')
        #f.write("message")
        print(self.channel)
        if not message:
            return
        if len(message) > 10000:
            return
        chnl_waiters = tuple(w for c, w in self.waiters if c == self.channel)
        for waiter in chnl_waiters:
                waiter.write_message((json.dumps({
                    "timestamp": int(time.time()),
                    "sender": self.sender_name,
                    "text": message
                })))

        thread = get_object_or_404(
            Thread,
            id=self.thread_id,
            participants__id=self.user_id
        )
        #partner = thread.participants.exclude(id=self.user_id)[0]
        #read = Read.objects.filter(user=partner, thread=Thread.objects.get(id=self.thread_id)).last()
        #if read:
            #if read.read == True:
                #read.read = FalseSSS
                #read.save()
        #if not read:
            #read = Read(user=partner, thread=Thread.objects.get(id=self.thread_id), read=False)
            #read.save()

        http_client = tornado.httpclient.AsyncHTTPClient()
        print('afer API')
        request = tornado.httpclient.HTTPRequest(
            "".join([
                        settings.SEND_MESSAGE_API_URL,
                        "/",
                        self.thread_id,
                        "/"
                    ]),
            method="POST",
            body=urllib.parse.urlencode({
                "message": message.encode("utf-8"),
                "api_key": settings.API_KEY,
                "sender_id": self.user_id
            })
        )
        print(request);
        http_client.fetch(request, self.handle_request)

    def show_new_message(self, result):
        self.write_message(str(result.body))

    def on_close(self):
        print('close!')
        try:
            self.waiters.remove((self.channel, self))
            #self.client.unsubscribe(self.channel)
        except AttributeError:
            pass
        def check():
            if self.client.connection.in_progress:
                tornado.ioloop.IOLoop.instance().add_timeout(
                    datetime.timedelta(0.00001),
                    check
                )
            else:
                self.client.disconnect()
        tornado.ioloop.IOLoop.instance().add_timeout(
            datetime.timedelta(0.00001),
            check
        )

application = tornado.web.Application([
    (r"/", MainHandler),
    (r'/(?P<thread_id>\d+)/', MessagesHandler),
])


