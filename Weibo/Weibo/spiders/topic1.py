#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-05-05 15:21:59
# @Last Modified by:   zengphil
# @Last Modified time: 2016-05-29 14:18:08

import time
import pickle
import random
import re
import numpy as np

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from datetime import datetime
from scrapy.http import FormRequest, Request

from Weibo.agents import AGENTS
from Weibo.items import WeiboItem
from Weibo.items import UserItem
from Weibo.items import CommentItem

class WeiboSpider(CrawlSpider):
    """docstring for WeiboSpider"""
    name = "topic1"
    # allow_domains = [
    #     "weibo.cn"
    # ]

    host = "http://weibo.cn"

    start_urls = [
        u'#苹果手机#',
    ]

    crawlID = set(start_urls)
    finishID = set()

    def start_requests(self):
        while True:
            contentID = self.crawlID.pop()
            self.finishID.add(contentID)

            return [FormRequest(url = "http://weibo.cn/search/", formdata = {'keyword': contentID, 'smblog': '搜微博'}, callback=self.parse_Content)]

    def parse_Content(self, response):
        """加载页面并提取目标URL"""
        pattern = pattern = re.compile(r'http://weibo.cn/[u/]{0,2}(\d+|\w+)')
        sel = Selector(response)
        Type = sel.xpath("//div/input[@name='keyword']/@value").extract_first()
        tweets = sel.xpath('body/div[@class="c" and @id]')
        for tweet in tweets:
            weiboItem = WeiboItem()
            id = tweet.xpath('@id').extract_first()
            name = tweet.xpath("div/a[@class='nk']/text()").extract_first()
            content = tweet.xpath('div/span[@class="ctt"]/text()').extract_first()  # 微博内容
            UserUrl = tweet.xpath("div/a[@class='nk']/@href").extract_first()
            like = re.findall(u'\u8d5e\[(\d+)\]', tweet.extract())
            repost = re.findall(u'\u8f6c\u53d1\[(\d+)\]', tweet.extract())
            comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.extract())
            others = tweet.xpath('div/span[@class="ct"]/text()').extract_first()

            weiboItem['ContentId'] = id
            weiboItem['Type'] = Type
            weiboItem['Name'] = name
            weiboItem['UID'] = re.findall(pattern, UserUrl)[0]
            if content:
                weiboItem["Content"] = content.strip(u"[\u4f4d\u7f6e]")
            if like:
                weiboItem["Like"] = str(like[0])
            if repost:
                weiboItem["Repost"] = str(repost[0])
            if comment:
                weiboItem["Comment"] = str(comment[0])
            if others:
                others = others.split(u"\u6765\u81ea")
                weiboItem["PostTime"] = others[0]
            print weiboItem['Content']
            yield weiboItem

        # Next Comment Information #
        Comment_urls = sel.xpath("//div/a[@class='cc' and @href]/@href").extract()
        for comment_url in Comment_urls:
            yield Request(url = comment_url, meta={"Type": Type}, callback = self.parse_Comment)

        # Next User Information #
        User_urls = sel.xpath("//div/a[@class='nk']/@href").extract()
        for user_url in User_urls:
            yield Request(url = user_url, callback = self.parse_User)

        # Next Content Page #
        Content_nextpage = sel.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()

        if Content_nextpage:
            yield Request(url=self.host + Content_nextpage[0],
                          callback=self.parse_Content)
        else:
            print 'No more Search Content!!!'


    def parse_Comment(self, response):
        """加载评论数据"""
        sel = Selector(response)
        tweets = sel.xpath('body/div[@class="c" and @id]')
        Type = response.meta["Type"]
        for tweet in tweets:
            Cond1 = tweet.xpath('a/@href').extract_first()
            if Cond1:
                commentItem = CommentItem()
                name = tweet.xpath('a/text()').extract_first()
                id = tweet.xpath('@id').extract_first()
                content = tweet.xpath('span[@class="ctt"]/text()').extract()
                uid = re.findall("uid=(\d+)", tweet.xpath("a[2]/@href").extract_first())[0]
                others = tweet.xpath('span[@class="ct"]/text()').extract_first()

                commentItem['Type'] = Type
                commentItem['Name'] = name
                commentItem['CommentId'] = id
                commentItem['UID'] = uid
                if len(content) > 1:
                    commentItem["Content"] = content[1].strip(u"[\u4f4d\u7f6e]")
                else:
                    commentItem["Content"] = content[0].strip(u"[\u4f4d\u7f6e]")
                if others:
                    others = others.split(u"\u6765\u81ea")
                    commentItem['PostTime'] = others[0]
                print commentItem["Content"]
                yield commentItem

        # Next User Information #
        User_urls = sel.xpath("//div[@class='c' and @id]/a[1]/@href").extract()
        for user_url in User_urls:
            if user_url:
                yield Request(url = self.host + user_url, callback = self.parse_User)

        # Next Comment Page #
        Comment_nextpage = sel.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()

        if Comment_nextpage:
            yield Request(url=self.host + Comment_nextpage[0],
                          callback=self.parse_Comment)
        else:
            print 'No more Search Comment!!!'


    def parse_User(self, response):
        """加载页面并提取用户信息"""
        sel = Selector(response)
        userItem = UserItem()
        FollowerUrl = sel.xpath("//div/a[contains(@href, 'follow')]/@href").extract_first()
        if FollowerUrl:
            userItem['UID'] = re.findall('\d{10}', FollowerUrl)[0]
        userItem['Name'] = sel.xpath("//div[@class='ut']/span[1]/text()").extract_first()
        text0 = sel.xpath("//div[@class='tip2']").extract_first()
        if text0:
            num_tweets = re.findall(u'\u5fae\u535a\[(\d+)\]', text0)
            num_follows = re.findall(u'\u5173\u6ce8\[(\d+)\]', text0)
            num_fans = re.findall(u'\u7c89\u4e1d\[(\d+)\]', text0)
            if num_tweets:
                userItem["TweetsNum"] = str(num_tweets[0])
            if num_follows:
                userItem["FollowersNum"] = str(num_follows[0])
            if num_fans:
                userItem["FansNum"] = str(num_fans[0])
        Follower = []
        if FollowerUrl:
            yield Request(url = self.host + FollowerUrl, meta={"item": userItem, "follower": Follower}, callback = self.parse_Follower)

    def parse_Follower(self, response):
        """提取用户粉丝数据"""
        userItem = response.meta['item']
        sel = Selector(response)
        text2 = sel.xpath(
            u'body//table/tr/td/a[text()="\u5173\u6ce8\u4ed6" or text()="\u5173\u6ce8\u5979"]/@href').extract()
        for element in text2:
            elem = re.findall('uid=(\d+)', element)
            if elem:
                response.meta['follower'].append(elem[0])

        url_nextpage = sel.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_nextpage:
            yield Request(url=self.host + url_nextpage[0], meta={"item": userItem, "follower": response.meta["follower"]},
                          callback=self.parse_Follower)
        else:
            Follower = response.meta['follower']
            userItem['CrawlFollowers'] = str(len(Follower))
            userItem['Follower'] = '.'.join(Follower)
            yield userItem


