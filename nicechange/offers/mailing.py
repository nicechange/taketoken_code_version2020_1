# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
import smtplib
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Mailing:

    # me = 'shnicechange@gmail.com'
    # # заголовок письма
    # subj = 'Уведомление от NiceChange'
    # # SMTP-сервер
    # server = "email-smtp.eu-west-1.amazonaws.com"
    # port = 25
    # user_name = "AKIAIXAV3WAGPHSTSNIA"
    # user_passwd = "AoEHxjkbngfxRQkuNDNctyw8MZ7bj7aXsCJmVZbKnXmp"

    me = 'taketokenotice@gmail.com'
    # заголовок письма
    subj = 'Уведомление от TakeToken'
    # SMTP-сервер
    server = "smtp.gmail.com"
    port = 587
    user_name = "taketokenotice@gmail.com"
    user_passwd = "elruibneqrbnoqeruberbqr"

    def send(self, message, email):
        # формирование сообщения
        msg = MIMEText(message, 'plain')
        msg['Subject'] = self.subj
        msg['From'] = self.me
        msg['To'] = email

        # отправка
        s = smtplib.SMTP(self.server, self.port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(self.user_name, self.user_passwd)
        s.sendmail(self.me, email, msg.as_string())
        s.quit()
