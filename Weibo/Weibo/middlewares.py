# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-03-11 17:09:06
# @Last Modified by:   fibears
# @Last Modified time: 2016-05-09 19:44:32

import random
from agents import AGENTS
from cookies import cookies

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







