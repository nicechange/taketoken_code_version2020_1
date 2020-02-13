from django.core.management.base import BaseCommand
from offers.models import Proffer, BurseCourse, Reply, FinishedDeals
from offers.burses import update
from datetime import timedelta
from datetime import datetime
from bitcoinrpc.authproxy import AuthServiceProxy
from accounts.models import Admins
from accounts.models import Notifications
from templated_email import send_templated_mail

class Command(BaseCommand):
    args = ''
    help = 'Update courses with base'

    def handle(self, *args, **options):
        update()
        for p in Proffer.objects.all():
            if p.prc != None and p.brs != None:
                type = 'ПРОДАЖА'
                if p.type == 'КУПЛЮ':
                    type = 'ПОКУПКА'
                bc = (BurseCourse.objects.filter(burse=p.brs, token='BTC').last()).course
                if type == "ПОКУПКА":
                    p.rate = int(bc - float(bc)/100*p.prc)
                else:
                    p.rate = int(bc + float(bc) / 100 * p.prc)
                p.save()

        for r in Reply.objects.all():
            if datetime(r.date.year, r.date.month, r.date.day, r.time.hour, r.time.minute, r.time.second) + timedelta(hours=1, minutes=30) < datetime.now():
                th = r.thread
                bl = th.bl
                conn = AuthServiceProxy("http://%s:%s@195.131.139.14:8332" % ('nicechange', 'nicechange'))
                if float(conn.getbalance(th.twallet)) > 0:
                    bl.blocked = bl.blocked - round(float(th.quantity), 8)
                    admi = Admins.objects.all().last()
                    per = round(float(th.quantity), 8) / 100 * float(admi.percent)
                    bl.fee = bl.fee - per
                    bl.save()
                    proffer = r.proffer
                    proffer.replies_count = proffer.replies_count - 1
                    proffer.save()
                    conn.move(th.twallet, th.destwallet, th.quantity)
                    fd = FinishedDeals.objects.create(user=proffer.user, bank=proffer.bank, quantity=r.quantity,
                                                      partner=r.user.username, price=r.price, status="Просрочена")
                    fd.save()
                    fd = FinishedDeals.objects.create(user=r.user, bank=proffer.bank, quantity=r.quantity,
                                                      partner=proffer.user.username, price=r.price, status="Просрочена")
                    fd.save()
                    if Notifications.objects.get(user=proffer.user).support == True:
                        send_templated_mail(
                            template_name="overdue.html",
                            from_email='from@example.com',
                            recipient_list=[proffer.user.email],
                            context={
                                'username': proffer.user.username
                            },

                        )
                    if Notifications.objects.get(user=r.user).support == True:
                        send_templated_mail(
                            template_name="overdue.html",
                            from_email='from@example.com',
                            recipient_list=[r.user.email],
                            context={
                                'username': r.user.username
                            },

                        )
                    th.delete()
                r.delete()






