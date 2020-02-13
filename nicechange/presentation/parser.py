# -*- coding: utf-8 -*-

import random
import re
import ssl
import time
import urllib
#from urllib.request import HTTPError

import requests
import schedule
from bs4 import BeautifulSoup
from lxml import html

from presentation.models import CBit, CLite, CEther


def choice(choice_pair = None):
    pair = {1:'Bitcoin/Альфа-Банк', 2:'Litecoin/Альфа-Банк', 3:'Ethereum/Альфа-Банк'}
    for key, val in pair.items():
        print(key, '-', val)
    while choice_pair not in pair.keys():
        choice_pair = int(input('\nВведите номер пары: '))
        if choice_pair == 1:
            url = 'https://www.bestchange.ru/bitcoin-to-alfaclick.html'
            modele = CBit
        elif choice_pair == 2:
            url = 'https://www.bestchange.ru/litecoin-to-alfaclick.html'
            modele = CLite
        elif choice_pair == 3:
            url = 'https://www.bestchange.ru/ethereum-to-alfaclick.html'
            modele = CEther
        else:
            print('Пары с таким номером нет в списке')
        print(choice_pair)
    return [url, modele]

def parser(url, modele):
    pars_res = {}
    i = 1
    get_pars = []
    j = 0
    session = requests.Session()
    session.trust_env = False
    print(url)
    r = session.get(url)
    print(r)
    r.encoding = 'cp1251'
    soup = BeautifulSoup(str(r.text), "lxml")

    info_block = soup.find('table', {'id':'content_table'})
    select_block = info_block.find_all('tr', {'onclick' : re.compile('^ccl')})

    sel_bl = re.compile(r'\d+\s+\d+\.\d+\s')
    get_all = re.findall(sel_bl, str(soup))
    tree = html.fromstring(r.text)

    info = ' '.join(tree.xpath('//*[@class="manual"]/span/text()[1]|//*[@class="manual"]/span/text()[2]')).split('.')
    info = info[:-1]


    for sel in select_block:
        name = sel.find('div', {'class':'ca'}).text
        link = sel.find('a', {'rel':'nofollow'}).get('href')
        req = urllib.request.Request(link, headers={'User-agent': 'Mozilla/5.0'})
        gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)  # Only for gangstars
        #try:
            #linkred = urllib.request.urlopen(req, timeout=120, context=gcontext).geturl()
           # print(linkred)
        #except HTTPError:
            #linkred = link
            #print(name, link)
            #continue
        pay = sel.find('div', {'class':'fs'}).text
        s = re.search(r'<span id="ld\d*">(.*)\.<\/span>', sel.text)
        get = tree.xpath('//*[@id="content_table"]/tbody/tr[{}]/td[4]/text()'.format(i))[0]
        reserve = sel.find('td', {'class':'ar arp'}).text
        for inf in info:
            pars_res[name] = [link, pay, get, reserve, inf]
        i += 1
    for key, val in pars_res.items():
        print(val)
        new = modele(name=key, link=val[0], pay=val[1], get=val[2], reserve=val[3], mode=val[4])
        new.save()
    return url

def start_parser():
    case = choice()
    parser(case[0], case[1])
    schedule.every(random.randint(120,180)).minutes.do(parser)

    while True:
        print('\nВ работе. Для выхода нажмите CTRL-C')
        schedule.run_pending()
        time.sleep(3600)
        print("ВЫбран данный URL: ", case[0])

    input("Press Enter")