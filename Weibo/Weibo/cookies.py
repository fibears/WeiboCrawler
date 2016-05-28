#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-05-05 15:21:59
# @Last Modified by:   zengphil
# @Last Modified time: 2016-05-28 21:39:22

import json
import base64
import requests


WeiBoAccount = [
    {'no': '13434323771', 'psw': 'a123456'},
    {'no': '17188348988', 'psw': 'a123456'},
    {'no': '13166795074', 'psw': 'a123456'},
    #{'no': '13166938986', 'psw': 'a123456'},
    {'no': '13072490894', 'psw': 'a123456'},
    {'no': 'paohuang75011@163.com', 'psw': 'aaa333'},
    {'no': 'yan94832858@163.com', 'psw': 'aaa333'},
]


def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
        postData = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        session = requests.Session()
        r = session.post(loginURL, data=postData)
        jsonStr = r.content.decode('utf-8')
        info = json.loads(jsonStr)
        if info["retcode"] == "0":
            print "Get Cookie Success!( Account:%s )" % account
            cookie = session.cookies.get_dict()
            cookies.append(cookie)
        else:
            print "Failed!( Reason:%s )" % info['reason']
    return cookies


cookies = getCookies(WeiBoAccount)
print "Get Cookies Finish!( Num:%d)" % len(cookies)
