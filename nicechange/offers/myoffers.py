from django.shortcuts import render
from offers.models import Order, Offer, Reply, Proffer, Course, Wallet, DealRole
from offers.offerstable import MyOffersTable, MyRepliesTable
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from offers.forms import TransactionForm
from offers.forms import TransactionForm
import bitcoinrpc
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from bitcoin import *
import threading
from privatemessages.models import Thread, Read

@login_required
def my_offers(request, item_id):
    offers = MyOffersTable(Offer.objects.filter(order=item_id))
    return render(request, 'offers.html', {'orders': offers})

@login_required
def my_replies(request, item_id):
    replies = MyRepliesTable(Reply.objects.filter(proffer=item_id))
    return render(request, 'offers.html', {'orders': replies})


@login_required(login_url='/login/')
def publish_order(request, item_id):
    order = Order.objects.get(id=item_id)
    order.state = 'Published'
    order.save()
    return HttpResponseRedirect('/cabinet/')

@login_required(login_url='/login/')
def publish_proffer(request, item_id):
    proffer = Proffer.objects.get(id=item_id)
    proffer.state = 'Published'
    proffer.save()
    from templated_email import send_templated_mail
    threading.Thread(target=send_templated_mail, args=("putoffer.html", 'from@example.com',
                                                       [request.user.email],
                                                       {
                                                           'username': request.user.username,
                                                           'token': proffer.type_of_token,
                                                           'rate': proffer.rate
                                                       }
                                                       )).start()
    return HttpResponseRedirect('/cabinet/')

@login_required(login_url='/login/')
def delete_course(request, item_id):
    course = Course.objects.get(id=item_id)
    course.delete()
    return HttpResponseRedirect('/courses/')

@login_required(login_url='/login/')
def delete_proffer(request, item_id):
    proffer = Proffer.objects.get(id=item_id)
    proffer.delete()
    return HttpResponseRedirect('/broker/')

@login_required(login_url='/login/')
def delete_wallet(request, item_id):
    wallet = Wallet.objects.get(id=item_id)
    wallet.delete()
    return HttpResponseRedirect('/wallets/')

@login_required(login_url='/login/')
def select_wallet(request, item_id):
    from privatemessages.models import ThreadActivity
    thread_id = ThreadActivity.objects.filter(user=request.user).last().thread.id
    wallet = Wallet.objects.get(id=item_id)
    dr = DealRole.objects.filter(user=request.user, thread=thread_id).last()
    dr.wallet = wallet
    dr.save()
    return HttpResponseRedirect('/deal/'+ str(thread_id))

def update_balances():
    conn = AuthServiceProxy("http://%s:%s@195.131.139.14:8332" % ('nicechange', 'nicechange'))
    for w in Wallet.objects.all():
        w.balance = format(conn.getbalance(w.address), 'f')
        w.save()

def open_wallet(request, item_id):
    form = TransactionForm
    wallet = Wallet.objects.get(id=item_id)
    priv = wallet.private_key
    pub = wallet.public_key
    btcaddr = wallet.btcaddress
    ethaddr = wallet.ethaddress
    h = history(btcaddr)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
             wlt = Wallet.objects.filter(btcaddress=form.cleaned_data['address'].__str__()).last()
             if wlt:
                 conn = AuthServiceProxy("http://%s:%s@195.131.139.14:8332" % ('nicechange', 'nicechange'))
                 conn.move(wallet.btcaddress, wlt.btcaddress, float(form.cleaned_data['quantity']))
                 threading.Thread(target=update_balances).start()
             else:
                 outs = [{'value': int(form.cleaned_data['quantity']), 'address': form.cleaned_data['address'].__str__()}]
                 tx = mktx(h, outs)
                 tx_ = sign(tx, 0, priv)
                 bytetx = tx_
                 conn = AuthServiceProxy("http://%s:%s@195.131.139.14:8332" % ('nicechange', 'nicechange'))
                 conn.settxfee(form.cleaned_data['fee'])
                 conn.sendrawtransaction(bytetx)
        return HttpResponseRedirect('/wallets/')
    return render(request, 'transaction.html', {'form': form, 'new_wallet':wallet, 'id':item_id})

