# coding: utf-8
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

    def open(self, user_id):
        session_key = self.get_cookie(settings.SESSION_COOKIE_NAME)
        session = session_engine.SessionStore(session_key)
        try:
            self.user_id = session["_auth_user_id"]
            self.sender_name = User.objects.get(id=self.user_id).username
        except (KeyError, User.DoesNotExist):
            self.close()
            return
        self.channel = user_id
        self.waiters.add((self))
        print(self.channel)
        print('выполнн')
        self.client.listen(self.show_new_message)

    def handle_request(self, response):
        pass

    def show_new_message(self, result):#python manage.py starttornadooffers
        print('ЗАЯВКА!')
        self.write_message(str(result.body))

    def on_message(self, message):
        print("message")
        for waiter in self.waiters:
            if waiter.channel == self.channel:
                waiter.write_message(message)
        print("message_send")

    def on_close(self):
        print('close!')
        try:
            self.waiters.remove((self))
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
    (r'/(?P<user_id>\d+)/', MessagesHandler),
])