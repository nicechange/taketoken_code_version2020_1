from offers.models import BurseCourse
from cryptocompy import coin
import requests
from pycbrf.toolbox import ExchangeRates

def upd():

    coin_data_btc = coin.get_coin_snapshot("BTC", "USD")['Exchanges']
    coin_data_eth = coin.get_coin_snapshot("ETH", "USD")['Exchanges']
    coin_data_ltc = coin.get_coin_snapshot("LTC", "USD")['Exchanges']

    course = 0
    for record in coin_data_btc:
        if record['MARKET'] == 'Bitfinex':
            course = record['PRICE']

    object = BurseCourse.objects.filter(burse='Bitfinex', token='BTC').last()
    if object:
        object.delete()
    object = BurseCourse(burse='Bitfinex', course=course, token='BTC')
    object.save()

    course = 0
    for record in coin_data_eth:
        if record['MARKET'] == 'Bitfinex':
            course = record['PRICE']

    object = BurseCourse.objects.filter(burse='Bitfinex', token='ETH').last()
    if object:
        object.delete()
    object = BurseCourse(burse='Bitfinex', course=course, token='ETH')
    object.save()

    course = 0
    for record in coin_data_ltc:
        if record['MARKET'] == 'Bitfinex':
            course = record['PRICE']

    object = BurseCourse.objects.filter(burse='Bitfinex', token='LTC').last()
    if object:
        object.delete()
    object = BurseCourse(burse='Bitfinex', course=course, token='LTC')
    object.save()

    course = 0
    for record in coin_data_btc:
        if record['MARKET'] == 'Kraken':
            course = record['PRICE']

    object = BurseCourse.objects.filter(burse='Kraken', token='BTC').last()
    if object:
        object.delete()
    object = BurseCourse(burse='Kraken', course=course, token='BTC')
    object.save()

    course = 0
    for record in coin_data_eth:
        if record['MARKET'] == 'Kraken':
            course = record['PRICE']

    object = BurseCourse.objects.filter(burse='Kraken', token='ETH').last()
    if object:
        object.delete()
    object = BurseCourse(burse='Kraken', course=course, token='ETH')
    object.save()

    course = 0
    for record in coin_data_ltc:
        if record['MARKET'] == 'Kraken':
            course = record['PRICE']

    object = BurseCourse.objects.filter(burse='Kraken', token='LTC').last()
    if object:
        object.delete()
    object = BurseCourse(burse='Kraken', course=course, token='LTC')
    object.save()

    course = 0
    for record in coin_data_btc:
        if record['MARKET'] == 'Poloniex':
            course = record['PRICE']

    object = BurseCourse.objects.filter(burse='Poloniex', token='BTC').last()
    if object:
        object.delete()
    object = BurseCourse(burse='Poloniex', course=course, token='BTC')
    object.save()

    course = 0
    for record in coin_data_eth:
        if record['MARKET'] == 'Poloniex':
            course = record['PRICE']

    object = BurseCourse.objects.filter(burse='Poloniex', token='ETH').last()
    if object:
        object.delete()
    object = BurseCourse(burse='Poloniex', course=course, token='ETH')
    object.save()

    course = 0
    for record in coin_data_ltc:
        if record['MARKET'] == 'Poloniex':
            course = record['PRICE']

    object = BurseCourse.objects.filter(burse='Poloniex', token='LTC').last()
    if object:
        object.delete()
    object = BurseCourse(burse='Poloniex', course=course, token='LTC')
    object.save()




def refr():
    usdru = ExchangeRates()['USD'].value
    for obj in BurseCourse.objects.all():
        obj.course = obj.course * float(usdru)
        obj.save()

def update():
    upd()
    refr()