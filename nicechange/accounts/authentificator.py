# -*- coding: utf-8 -*-
import pyotp
from accounts.forms import CodeAuthForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from accounts.models import AlreadyEnter
from offers.models import Reply, Wallet
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def getcode(request):
    return request.user.password

from django.contrib.auth import logout, login
def codeauth(request, user_):
    debug = ''
    key = ''
    if user_ == '0':
        if AlreadyEnter.objects.filter(user=request.user).last():
            key = AlreadyEnter.objects.filter(user=request.user).last().key
            user_=request.user.id
    else:
        if not User.objects.get(id=user_).profile.steptwo == True:
          return HttpResponseRedirect('/login/')
        if AlreadyEnter.objects.filter(user__id=user_).last():
            key = AlreadyEnter.objects.filter(user=User.objects.get(id=user_)).last().key
    totp = pyotp.TOTP(key)
    form = CodeAuthForm()
    msg = ""
    logout(request)
    if request.method == 'POST':
        form = CodeAuthForm(request.POST)
        if form.is_valid():
            debug = ''
            if form.cleaned_data['code'] == totp.now():
                olduser = User.objects.get(id=user_)
                login(request, user=olduser, backend='accounts.views.EmailAuthBackend')
                request.user.profile.steptwo = False
                request.user.profile.save()
                return HttpResponseRedirect('/nicechange/')
            else:
                msg = 'Неверный код'
        else:
            return render(request, 'registration/login_err.html')
    return render(request, 'codeauth.html', {"form":form, "msg":msg, "debug":debug, "user_":user_})

def codeauth2(request, deal):
    key = ''
    if AlreadyEnter.objects.filter(user=request.user).last():
        key = AlreadyEnter.objects.filter(user=request.user).last().key
    totp = pyotp.TOTP(key)
    form = CodeAuthForm()
    reply = Reply.objects.get(id=deal)
    if request.method == 'POST':
        form = CodeAuthForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] != totp.now():
                reply.trying = True
                reply.save()
            else:
                reply.trying = True
                reply.confirm = True
                reply.save()
            return HttpResponseRedirect('/deal/' +str(reply.thread.id)+'/')
    return render(request, 'codeauth2.html', {"form":form, "deal":deal})

def codeauth3(request, wal):
    key = ''
    if AlreadyEnter.objects.filter(user=request.user).last():
        key = AlreadyEnter.objects.filter(user=request.user).last().key
    totp = pyotp.TOTP(key)
    form = CodeAuthForm()
    wallet = Wallet.objects.get(id=wal)
    if request.method == 'POST':
        form = CodeAuthForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] != totp.now():
                wallet.trying = True
                wallet.save()
            else:
                wallet.trying = True
                wallet.confirm = True
                wallet.save()
            return HttpResponseRedirect('/wallet/' +str(wallet.id)+'/')
    return render(request, 'codeauth3.html', {"form":form, "wal":wal})

class EmailAuthBackend(object):
    name = 'dddwqdwq'
    @staticmethod
    def authenticate(email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return 'dwqdqwd'

        if not user.check_password(password):
            return 'fewfwef'

        return 'dewdwe'

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return 'dwqdwq'