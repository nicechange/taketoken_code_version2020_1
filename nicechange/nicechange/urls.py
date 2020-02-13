"""nicechange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import accounts.views
import burse.views
import offers.views
import privatemessages.views
from presentation import views
from privatemessages import urls as msg_urls
from privatemessages.views import send_message_view, send_message_api_view

from django.conf import settings
admin.site.site_title = settings.ADMIN_SITE_HEADER
admin.site.site_header = settings.ADMIN_SITE_HEADER
from presentation import views
from accounts import views as accounts_views
from presentation.views import gcounter


urlpatterns = [
    url(r'^popup/$', views.popup),
    url(r'^admin/', admin.site.urls),
    url(r'^prepare/', accounts_views.if_first),
    #url(r'^$', burse.views.main_page),
    url(r'^stat/(?P<user>\d+)/$', burse.views.stat),
    url(r'^$', views.main_page),
    url(r'^nicechange/(?P<forbidden>\D+)/$', burse.views.main_page),
    url(r'^nicechange/(?P<usr>\d+)/$', burse.views.main_page),
    url(r'^nicechange/$', burse.views.main_page),
    url(r'^login/$', accounts.views.login),
    url(r'^register/$', accounts.views.RegisterFormView.as_view()),
    url(r'^index/$', burse.views.main_page),
    url(r'^order/$', offers.views.add_order),
    url(r'^proffer/$', offers.views.add_proffer),
    url(r'^my/$', offers.views.my_orders),
    url(r'^user/$', offers.views.user),
    url(r'^cabinet/$', offers.views.cabinet),
    url(r'^broker/(?P<thread_id>\d+)/$', offers.views.broker, name="offers.views.broker"),
    url(r'^broker/$', offers.views.broker),
    url(r'^replies/$', offers.views.replies),
    url(r'^mybrok/$', offers.views.my_for_broker),
    url(r'^my/(?P<item_id>\d+)/$', offers.myoffers.my_offers),
    url(r'^mybrok/(?P<item_id>\d+)/$', offers.myoffers.my_replies),
    url(r'^dealstartorder/(?P<item_id>\d+)/$', offers.deals.deal_start_order),
    url(r'^dealstartproffer/(?P<item_id>\d+)/$', offers.deals.deal_start_proffer),
    url(r'^offer/$', offers.views.reply),
    url(r'^reply/(?P<item_id>\d+)/$', offers.views.reply),
    url(r'^answer/(?P<item_id>\d+)/$', offers.views.answer),
    url(r'^publor/(?P<item_id>\d+)/$', offers.myoffers.publish_order),
    url(r'^bublpr/(?P<item_id>\d+)/$', offers.myoffers.publish_proffer),
    url(r'^messages/', include((msg_urls, 'messages'), namespace='messages')),
    url(r'^messages/send_message/', send_message_view),
    url(r'^send_message_api/(?P<thread_id>\d+)/$', send_message_api_view),
    url(r'^google8d4ad422bb0bd56a.html', gcounter),
    url(r'^chat/(?P<thread_id>\d+)/$', privatemessages.views.chat_view, name="privatemessages.views.chat_view"),
    url(r'helpdesk/', include('helpdesk.urls')),
    url(r'^courses/', offers.views.show_courses),
    url(r'^delcourse/(?P<item_id>\d+)/$', offers.myoffers.delete_course),
    url(r'^delprof/(?P<item_id>\d+)/$', offers.myoffers.delete_proffer),
    url(r'^update/', views.update),
    url(r'^updcourses/', offers.views.update_courses),
    url(r'^notifications/', accounts_views.notifications_view),
    url(r'^wallets/$', offers.views.wallets),
    url(r'^wallet/(?P<item_id>\d+)/$', offers.myoffers.open_wallet),
    url(r'^delwallet/(?P<item_id>\d+)/$', offers.myoffers.delete_wallet),
    url(r'^account/', include('social_django.urls', namespace='social')),
    url(r'^account/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    url(r'^logout/', burse.views.Logout),
    url(r'^codeauth/(?P<user_>\d+)/$', accounts.authentificator.codeauth),
    url(r'^profile/', burse.views.update_profile),
    url(r'^deal/(?P<thread_id>\d+)/$', offers.views.deal),
    url(r'^selwallet/(?P<item_id>\d+)/$', offers.myoffers.select_wallet),
    url(r'^auth_qr_code/(?P<auth_code>.+)/$', accounts.views.auth_qr_code),
    url(r'^rspwn/', accounts.views.rspwn),
    url(r'^admins/', accounts.views.admins),
    url(r'^apromo/', accounts.views.apromo),
    url(r'^promo/', offers.views.promo),
    url(r'^history/', accounts.views.history),
    url(r'^deldeal/(?P<item_id>\d+)/$', offers.views.delete_deal),
    url(r'^delfdeal/(?P<item_id>\d+)/$', offers.views.delete_fdeal),
    url(r'^codeauth2/(?P<deal>\d+)/$', accounts.authentificator.codeauth2),
    url(r'^codeauth3/(?P<wal>\d+)/$', accounts.authentificator.codeauth3),
]


from django.contrib.flatpages import views

urlpatterns += [
    url(r'^about/$', views.flatpage, {'url': '/about/'}),
    url(r'^help/$', views.flatpage, {'url': '/help/'}),
    url(r'^purse/$', views.flatpage, {'url': '/purse/'}),
    url(r'^token/$', views.flatpage, {'url': '/token/'}),

    url(r'^aboutservise/$', views.flatpage, {'url': '/aboutservise/'}),
    url(r'^rules/$', views.flatpage, {'url': '/rules/'}),
    url(r'^news/$', views.flatpage, {'url': '/news/'}),
    url(r'^aboutus/$', views.flatpage, {'url': '/aboutus/'}),
    url(r'^users/$', views.flatpage, {'url': '/users/'}),
    url(r'^rulesserv/$', views.flatpage, {'url': '/ruleserv/'}),
    url(r'^answers/$', views.flatpage, {'url': '/answers/'}),
    url(r'^vocub/$', views.flatpage, {'url': '/vocub/'}),
    url(r'^instruction/$', views.flatpage, {'url': '/instruction/'}),
    url(r'^security/$', views.flatpage, {'url': '/security/'}),
    url(r'^forum/$', views.flatpage, {'url': '/forum/'}),
]