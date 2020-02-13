# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView
import accounts.forms
from accounts.forms import NotificationsForm, PrepareFirstForm
from accounts.models import Notifications, AlreadyEnter
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import threading
from accounts.authentificator import getcode
from bitcoin import *
from accounts.forms import RspwnForm, AdminsForm, PromoForm
from accounts.models import User, Admins, Promo
from offers.models import FinishedDeals



class RegisterFormView(FormView):
    form_class = accounts.forms.CreateUserForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        user = form.save(commit=False)
        em = user.email
        if User.objects.filter(email=em).count() > 0:
             return render(self.request, 'registration/login_erre.html')
        user.save()
        broker = self.request.POST.getlist('broker')
        if broker!=[]:
            if broker[0] == 'on':
                g = Group.objects.get(name='broker')
                g.user_set.add(user)
        # Вызываем метод базового класса
        text = "Привет!"
        from templated_email import send_templated_mail
        threading.Thread(target=send_templated_mail, args=("registration.html",
                                                           'from@example.com', [user.email],
                                                           {
                                                               'username': user.username
                                                           }
                                                           )).start()

        return super(RegisterFormView, self).form_valid(form)

class EmailAuthBackend(object):
    name = 'mybackend'
    @staticmethod
    def authenticate(email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if not user.check_password(password):
            return None

        return user

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

from django.contrib.auth import login as lgn
def login(request):
    from accounts.forms import LoginForm
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = EmailAuthBackend.authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is None:
                return render(request, 'registration/login_err.html')
            else:
                lgn(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect('/prepare/')
        else:
            return HttpResponseRedirect('/account/login/')
    return render(request, 'registration/login.html', {"form": form})

def notifications_view(request):
    if Notifications.objects.filter(user=request.user):
        form = NotificationsForm(instance=Notifications.objects.get(user=request.user))
    else:
        form = NotificationsForm()
    if request.method == 'POST':
        form = NotificationsForm(request.POST)
        if form.is_valid():
            for object in Notifications.objects.filter(user=request.user):
                object.delete()
            approve = form.save(commit=False)
            approve.user = request.user
            approve.save()
    return render(request, 'alerts.html', {"form":form})

import os
import string
import qrcode
from django.http import HttpResponse
import random

def make_qr_code(string):
    return qrcode.make(string, box_size=10, border=1)
import base64
def generate_random_string(request):
    """
    Returns a string with `length` characters chosen from `stringset`
    """
    #return (base64.b32encode(bytes(''.join(random.choices(string.hexdigits, k=16)).encode()))).__str__()[2:18]
    return str(base64.b32encode(random.getrandbits(80).to_bytes(16, 'little')))[2:18]


def auth_qr_code(request, auth_code):
    img = make_qr_code("otpauth://totp/"+request.user.username + "@taketoken.net?secret=" + request.GET['secret'].__str__())
    response = HttpResponse(content_type="image/jpeg")
    img.save(response, "PNG")
    return response

@login_required
def if_first(request):
    import pyotp
    from burse.models import Profile
    if AlreadyEnter.objects.filter(user=request.user).last():
        account = Profile.objects.filter(user=request.user).last()
        if account.two == False:
            return HttpResponseRedirect('/nicechange')
        else:
            request.user.profile.steptwo = True
            request.user.profile.save()
            return HttpResponseRedirect('/codeauth/0/')
    from offers.models import Wallet
    from bitcoinrpc.authproxy import AuthServiceProxy
    pk = sha256(Wallet.objects.count().__str__() + request.user.password)
    pub = privtopub(pk)
    addr = pubtoaddr(pub)
    import sha3
    obj = Notifications.objects.create(user=request.user, support=True, chat=True, deal=True, reply=True)
    obj.save()
    keccak = sha3.keccak_256()
    keccak.update(pub.encode())
    ethaddr = "0x" + str(keccak.hexdigest()[24:])
    wifKey = encode_privkey(pk, 'wif')
    conn = AuthServiceProxy("http://%s:%s@188.134.66.68:8332" % ('nicechange', 'nicechange'))
    conn.importprivkey(wifKey.__str__(), addr.__str__(), False)
    wallet = Wallet(private_key=wifKey, public_key=pub, btcaddress=addr, ethaddress=ethaddr, user=request.user)
    wallet.save()
    form = PrepareFirstForm()
    secret = getcode(request)
    key = generate_random_string(request)
    object = AlreadyEnter(user=request.user)
    object.key = key
    object.save()
    #g = Group.objects.get(name='broker')
    #g.user_set.add(request.user)
    #g.save()
    link = pyotp.totp.TOTP(key).provisioning_uri(request.user.username)
    if request.method == 'POST':
        form = PrepareFirstForm(request.POST)
        #if form.is_valid():
        #if form.cleaned_data['type'] == 'broker':
        #g = Group.objects.get(name='broker')
        #g.user_set.add(request.user)
        if form.cleaned_data['key']:
            object.key = form.cleaned_data['key']
            object.save()
        return   HttpResponseRedirect('/codeauth')
    return render(request, 'prepare.html', {"form":form, "secret":secret, "auth_code":link})


from django.contrib.auth import logout
def social_user(backend, uid, user=None, *args, **kwargs):
    '''OVERRIDED: It will logout the current user
    instead of raise an exception '''

    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            logout(backend.strategy.request)
            #msg = 'This {0} account is already in use.'.format(provider)
            #raise AuthAlreadyAssociated(backend, msg)
        elif not user:
            user = social.user
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}

from templated_email import send_templated_mail
def rspwn(request):
    form = RspwnForm()
    if request.method == 'POST':
        form = RspwnForm(request.POST)
        if form.data['login']:
            u = User.objects.filter(username=form.data['login']).last()
            if not u:
                u = User.objects.filter(email=form.data['login']).last()
            if not u:
                return render(request, 'noaccount.html', {"form": form})
            user = u
            import os, random, string
            length = 13
            chars = string.ascii_letters + string.digits + '!@#$%^&*()'
            random.seed = (os.urandom(1024))
            password = ''.join(random.choice(chars) for i in range(length))
            user.set_password(password)
            user.save()
            send_templated_mail(
                template_name="rspwn.html",
                from_email='from@example.com',
                recipient_list=[user.email],
                context={
                    'password': password
                },

            )
            return render(request, 'rspwnsucess.html')
    return render(request, 'rspwn.html', {"form": form})

def admins(request):
    form = AdminsForm(instance=Admins.objects.last())
    if request.method == 'POST':
        if "history" in request.POST:
            return HttpResponseRedirect('/history/')
        form = AdminsForm(request.POST)
        if form.is_valid():
            obj = Admins.objects.last()
            if obj:
                obj.delete()
            form.save()
    ins = Admins.objects.last()
    all = ins.sum
    if ins.walletsum == None:
        ins.walletsum = 0
    ws = round(float(ins.walletsum), 8)
    ct = ins.count
    return render(request, 'admins.html', {"form": form, "all":all, "ws":ws, "ct":ct})



def history(request):
    finished_deals = FinishedDeals.objects.all()
    return render(request, 'history.html', {"finished_deals":finished_deals})


from accounts.tables import CodesTable
def apromo(request):
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')
    form = PromoForm()
    valid = ''
    if request.method == 'POST':
        form = PromoForm(request.POST)
        if form.is_valid():
            pcode = form.save(commit=False)
            pcode.save()
    pcodes = CodesTable(Promo.objects.all())
    return render(request, 'apromo.html', {'codes': pcodes, 'form': form, 'valid': valid})