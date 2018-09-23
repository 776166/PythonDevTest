#!/usr/bin/env python

import urllib.request
from bs4 import BeautifulSoup
import ssl

LINK = 'https://breffi.ru/ru/about'

def get_link_data(link):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        f = urllib.request.urlopen(LINK, context=ctx)
    except:
        # print('Very Bad Link')
        return False
    # print('Very Good Link')
    data = f.read()
    f.close()
    return data

def worth(request):
    page_data = get_link_data(LINK)
    soup = BeautifulSoup(page_data, 'html.parser')

    worth = soup.find('div', {'class':'content-section worth'})
    # print(worth)

    soup = BeautifulSoup(str(worth), 'html.parser')

    titles = soup.findAll('div', {'class':'content-section__itemtitle'})
    texts = soup.findAll('div', {'class':'content-section__itemtext'})

    i = 0
    worth = []
    while i < 5:
        # print('0%d %s // %s' % (i+1, titles[i].text, texts[i].text))
        worth.append({'title':titles[i].text, 'text':texts[i].text})
        i += 1
    return worth
