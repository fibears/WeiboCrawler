#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-05-05 15:21:59
# @Last Modified by:   fibears
# @Last Modified time: 2016-05-09 13:47:10

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
        self.driver.get(self.url)
        for cookie in self.cookieweibo:
            self.driver.add_cookie(cookie)

    def parse(self, response):
        self.logger.info("This url has been identified - " + response.url)
        self.driver.get(response.url)
        myhtml = self.driver.page_source
        self.driver.close()
        print myhtml
        return myhtml










