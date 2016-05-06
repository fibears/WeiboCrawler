# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-03-11 17:09:06
# @Last Modified by:   zengphil
# @Last Modified time: 2016-05-06 15:38:22

import random
from agents import AGENTS

class CustomUserAgentMiddleware(object):
    """docstring for CustomUserAgentMiddleware"""
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent








