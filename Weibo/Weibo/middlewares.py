# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-03-11 17:09:06
# @Last Modified by:   zengphil
# @Last Modified time: 2016-05-29 14:18:48

import base64
import random
from agents import AGENTS
from cookies import cookies

# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Get proxy
        with open('Weibo/proxy.txt', 'r') as p:
            proxies = p.readlines()

        proxy = random.choice(proxies).strip("\n")
        # Set the location of the proxy
        request.meta['proxy'] = "http://" + proxy

        # # Use the following lines if your proxy requires authentication
        # proxy_user_pass = "USERNAME:PASSWORD"
        # # setup basic authentication for the proxy
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

# Change User-Agent #
class CustomUserAgentMiddleware(object):
    """docstring for CustomUserAgentMiddleware"""
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent

# Change Cookie #
class CustomCookieMiddleware(object):
    """docstring for CustomCookieMiddleware"""
    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        request.cookies = cookie


