# -*- coding: utf-8 -*-
from django.shortcuts import render
from presentation.forms import AddUserMailForm, ContactForm
from presentation.coursetable import CourseBitTable, CourseLiteTable, CourseEtherTable
from presentation.models import CBit, CLite, CEther, FutureUser
from offers.mailing import Mailing
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from presentation.update import start_parser
from django.http import HttpResponse, HttpResponseRedirect
import datetime

def gcounter(request):
    return render(request, 'google8d4ad422bb0bd56a.html')

def update(request):
    start_parser()
    return HttpResponseRedirect(
        '/test/')


def main_page(request):
    mailer = Mailing
    date = datetime.datetime.now().date()
    form = AddUserMailForm
    tableBit = CourseBitTable(CBit.objects.all())
    tableLite = CourseLiteTable(CLite.objects.all())
    tableBit.order_by = 'get'
    tableEther = CourseEtherTable(CEther.objects.all())
    tabs = [True,False,False]
    if request.method == 'GET':
        r = request.GET
        form = AddUserMailForm(request.GET)
        if form.is_valid():
            form.save()
            mailer.send(self=Mailing,
                        message='Здравствуйте! До открытия биржи осталось совсем недолго, '
                                'и вы узнаете об этом среди первых! Спасибо вам за доверие!',
                        email=FutureUser.objects.last().email)
            mailer.send(self=Mailing, message='Еще один пользователь подписался сейчас на TakeToken.',
                        email='nicechangenicechange@gmail.com')
        if r.__contains__('sort'):
            tableBit = CourseBitTable(CBit.objects.all())
            tableBit.order_by = r.__getitem__('sort')
            tableLite = CourseLiteTable(CLite.objects.all())
            tableBit.order_by = r.__getitem__('sort')
            tableEther = CourseEtherTable(CEther.objects.all())
            tableBit.order_by = r.__getitem__('sort')
    if request.method == 'POST':
        form = AddUserMailForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'index.html',  {'form': form, 'table_bit': tableBit, 'table_lite': tableLite, 'table_ether': tableEther,
                                           'date':date, 'tabs':tabs})




def contactView(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		#Если форма заполнена корректно, сохраняем все введённые пользователем значения
		if form.is_valid():
			sender = form.cleaned_data['sender']
			message = form.cleaned_data['message']
			copy = form.cleaned_data['copy']

			recipients = ['shnicechange@gmail.com']
			#Если пользователь захотел получить копию себе, добавляем его в список получателей
			if copy:
				recipients.append(sender)
			try:
				send_mail(u'Обратная связь Taketoken', message, 'taketokenotice@gmail.com', recipients)
			except BadHeaderError: #Защита от уязвимости
				return HttpResponse('Invalid header found')
			#Переходим на другую страницу, если сообщение отправлено
			return render(request, 'thanks.html')
	else:
		#Заполняем форму
		form = ContactForm()
	#Отправляем форму на страницу
	return render(request, 'contact.html', {'form': form})

def popup(request):
    return render(request, 'popup.html')