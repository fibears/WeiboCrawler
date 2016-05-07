#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zengphil
# @Date:   2016-05-05 15:21:59
# @Last Modified by:   fibears
# @Last Modified time: 2016-05-07 11:34:33

import time
import pickle

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from datetime import datetime
from scrapy.http import FormRequest, Request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Weibo.items import WeiboItem
from Weibo.items import UserItem

class WeiboSpider(CrawlSpider):
    """docstring for WeiboSpider"""
    name = "Weibo"
    allow_domains = [
        "m.weibo.cn"
    ]
    start_urls = [
        "http://m.weibo.cn/searchs"
    ]

    def __init__(self):
        with open("Weibo/cookie.txt", "r") as f:
            self.cookieweibo = pickle.load(f)
        self.driver = webdriver.PhantomJS()
        self.url = "http://m.weibo.cn/u/1984250112"
        self.loginurl = 'https://passport.weibo.cn/sso/login'
        self.driver.get(self.url)
        for cookie in self.cookieweibo:
            self.driver.add_cookie(cookie)
        # headers for Request #
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0)',
        'Host': 'passport.weibo.cn',
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F'
        }

    def start_requests(self):
        return [Request(self.loginurl, meta = {'cookiejar' : 1}, callback = self.post_login)]

    def post_login(self, response):
        return [FormRequest.from_response(response,
            meta = {'cookiejar' : response.meta['cookiejar']},
            headers = self.headers,  #注意此处的headers
            formdata = {
            'email': '250609365@qq.com',
            'password': 'wunai123'
            },
            callback = self.after_login,
            dont_filter = True
        )]

    def after_login():
        pass

    def parse(self, response):
        self.logger.info("This url has been identified - " + response.url)
        self.driver.get(response.url)
        myhtml = self.driver.page_source
        self.driver.close()
        print myhtml
        return myhtml










