#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-05-05 15:21:59
# @Last Modified by:   fibears
# @Last Modified time: 2016-05-12 19:42:03

import time
import pickle
import random
import re
import numpy as np

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from datetime import datetime
from scrapy.http import FormRequest, Request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Weibo.sqldata import SQL_ContentUrl, SQL_UserUID

from Weibo.agents import AGENTS
from Weibo.items import WeiboItem
from Weibo.items import UserItem

class WeiboSpider(CrawlSpider):
    """docstring for WeiboSpider"""
    name = "Weibo"
    allow_domains = [
        "m.weibo.cn"
    ]
    search_content = u'西二旗'

    start_urls = [
        "http://m.weibo.cn/k/" + search_content + '?from=feed'
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
        """加载页面并提取目标URL"""
        self.driver.get(response.url)
        for i in xrange(1,30):
            time.sleep(5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Extract Content URL #
        URL1 = self.driver.find_elements_by_xpath("//div[contains(@class,'line-around')]")
        ContentURL = []
        for i in xrange(0, len(URL1)):
            if URL1[i].get_attribute('data-jump') != None:
                print URL1[i].get_attribute('data-jump')
                ContentURL.append('http://m.weibo.cn' + URL1[i].get_attribute('data-jump'))
        # Extract Users URL #
        URL2 = self.driver.find_elements_by_xpath("//div[contains(@class,'line-around')]/header/a[contains(@class, 'mod-media')]")
        UserURL = []
        for i in xrange(0, len(URL2)):
            if URL2[i].get_attribute('href') != None:
                print URL2[i].get_attribute('href')
                UserURL.append(URL2[i].get_attribute('href'))

        # Parse URL By Different Parse Function #
        for content_url in ContentURL:
            if content_url not in SQL_ContentUrl:
                headers = {
                'User-Agent': random.choice(AGENTS),
                'Host': 'm.weibo.cn',
                'Referer': content_url
                }
                yield Request(url = content_url, headers = headers, callback = self.parseContent)

        for user_url in UserURL:
            pattern = re.compile(r'http://m.weibo.cn/u/(\d{10})')
            uid = re.findall(pattern, user_url)[0]
            """判断该用户是否存在数据库中"""
            if uid not in SQL_UserUID:
                headers = {
                'User-Agent': random.choice(AGENTS),
                'Host': 'm.weibo.cn',
                'Referer': user_url
                }

                yield Request(url = user_url, headers = headers, callback = self.parseUser)

    # Parse Content Information #
    def parseContent(self, response):
        self.logger.info("Parse ContentInformation!!!")
        self.logger.info("This url has been identified - " + response.url)
        self.driver.get(response.url)
        pattern = re.compile(r'http://m.weibo.cn/(\d{10})/.*?')
        # Weibo Content #
        weiboItem = WeiboItem()
        time.sleep(2)
        weiboItem['Url'] = response.url
        weiboItem['Name'] = self.driver.find_element_by_xpath("//div[@class='box-col item-list']/a/span").text
        weiboItem['Content'] = self.driver.find_elements_by_xpath("//a[@href='/k/西二旗?from=feed']/..")[0].text
        weiboItem['UID'] = re.findall(pattern, response.url)[0]
        weiboItem['Repost'] = self.driver.find_element_by_xpath("//span[@data-node='repost']/em").text
        weiboItem['Comment'] = self.driver.find_element_by_xpath("//span[@data-node='comment']/em").text
        weiboItem['Like'] = self.driver.find_element_by_xpath("//span[@data-node='like']/em").text
        weiboItem['PostTime'] = self.driver.find_element_by_xpath("//span[@class='time']").text
        # self.driver.close()
        yield weiboItem

    # Parse Users Information #
    def parseUser(self, response):
        self.logger.info("Parse UserInformation!!!")
        self.logger.info("This url has been identified - " + response.url)
        self.driver.get(response.url)
        pattern = re.compile(r'http://m.weibo.cn/u/(\d{10})')
        # User Information #
        userItem = UserItem()
        time.sleep(2)
        userItem['UID'] = re.findall(pattern, response.url)[0]
        userItem['Name'] = self.driver.find_element_by_xpath("//div[@class= 'item-main txt-xl txt-cut']/span").text
        userItem['FansNum'] = self.driver.find_element_by_xpath("//a[contains(@href, 'FANS')]/div[@class='mct-a txt-s']").text
        FollowerNum = self.driver.find_element_by_xpath("//a[contains(@href, 'FOLLOWERS')]/div[@class='mct-a txt-s']").text
        userItem['FollowerNum'] = FollowerNum

        # New Page #
        FollowerUrl = 'http://m.weibo.cn/page/tpl?containerid=' + u'1005051' + re.findall(pattern, response.url)[0] + '_-_FOLLOWERS'
        self.driver.get(FollowerUrl)
        time.sleep(3)
        for i in xrange(1,(np.int(FollowerNum)/10)+7):
            time.sleep(5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        Users = self.driver.find_elements_by_xpath("//div[@class='layout-box media-graphic']/a[1]")
        UserList = [re.findall(pattern, user.get_attribute('href'))[0]  for user in Users]
        userItem['Follower'] = '.'.join(UserList)

        yield userItem








