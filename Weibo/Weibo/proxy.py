#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zengphil
# @Date:   2016-05-29 09:47:54
# @Last Modified by:   zengphil
# @Last Modified time: 2016-05-29 14:39:58

import urllib2
import socket
from bs4 import BeautifulSoup

def IsOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except Exception:
        return False

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0'
}
url = 'http://www.xicidaili.com/nn/'
hurl = urllib2.Request(url, headers=header)

html_doc = urllib2.urlopen(hurl).read()
soup = BeautifulSoup(html_doc, 'lxml')
trs = soup.find('table', id='ip_list').find_all('tr')
for tr in trs[1:]:
    tds = tr.find_all('td')
    ip = tds[1].text.strip()
    port = tds[2].text.strip()
    protocol = tds[5].text.strip()
    if protocol == 'HTTP' or protocol == 'HTTPS':
        print ip
        if IsOpen(ip, port):
            print ip + ':' + port + 'is OK'
            with open('proxy.txt','a') as proxy:
                proxy.write(ip + ":" + port + "\n")


