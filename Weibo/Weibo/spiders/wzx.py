#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-05-05 15:21:59
# @Last Modified by:   fibears
# @Last Modified time: 2016-05-09 23:32:33

import time
import pickle
import random

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from datetime import datetime
from scrapy.http import FormRequest, Request
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Weibo.agents import AGENTS
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
    search_content = u'#西二旗#'

    def __init__(self):
        with open("Weibo/cookie.txt", "r") as f:
            self.cookieweibo = pickle.load(f)
        self.driver = webdriver.PhantomJS()
        self.url = "http://m.weibo.cn/u/1984250112"
        self.driver.get(self.url)
        for cookie in self.cookieweibo:
            self.driver.add_cookie(cookie)


    def parse(self, response):
        """加载页面并提取目标URL"""
        self.driver.get(response.url)
        Searchs = self.driver.find_element_by_xpath("//input[@name='queryVal']")
        Searchs.send_keys(self.search_content)
        Searchs.send_keys(Keys.ENTER)
        Page = self.driver.find_element_by_xpath('//*[@class="module-topbar"]/a[2]')
        for i in xrange(1,10):
            time.sleep(2)
            Page.send_keys(Keys.PAGE_DOWN)

        # Extract Content URL #
        URL1 = self.driver.find_elements_by_xpath("//div[contains(@class,'line-around')]")
        ContentURL = []
        for i in xrange(0, len(URL1)):
            if URL1[i].get_attribute('data-jump') != None:
                print URL1[i].get_attribute('data-jump')
                ContentURL.append('http://m.weibo.cn' + URL1[i].get_attribute('data-jump'))
        # Extract Users URL #
        URL2 = self.driver.find_elements_by_xpath("//a[@class='mod-media size-xs']")
        UserURL = []
        for i in xrange(0, len(URL2)):
            if URL2[i].get_attribute('href') != None:
                UserURL.append(URL2[i].get_attribute('href'))

        self.driver.close()
        # Parse URL By Different Parse Function #
        for content_url in ContentURL:
            headers = {
            'User-Agent': random.choice(AGENTS),
            'Host': 'm.weibo.cn',
            'Referer': content_url
            }
            yield Request(url = content_url, headers = headers, callback = self.parseContent)
        # for user_url in UserURL:
        #     yield Request(url = user_url, callback = self.parseUser)

    # Parse Content Information #
    def parseContent(self, response):
        self.logger.info("This url has been identified - " + response.url)
        # Mydriver = self.driver
        # Mydriver.get(response.url)
        # Weibo Content #
        weiboItem = WeiboItem()
        # print response
        selector = Selector(response)

        content = selector.xpath("//p[contains(@href,'feed')]/../text()").extract()
        print content
        # Mydriver.close()
        return weiboItem

    # Parse Users Information #








