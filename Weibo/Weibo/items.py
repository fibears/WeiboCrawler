# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Url = scrapy.Field()
    Content = scrapy.Field()
    UID = scrapy.Field()
    Repost = scrapy.Field()
    Comment = scrapy.Field()
    Like = scrapy.Field()
    PostTime = scrapy.Field()

class UserItem(scrapy.Item):
    Url = scrapy.Field()
    UID = scrapy.Field()
    Name = scrapy.Field()
    FansNum = scrapy.Field()
    FollowerNum = scrapy.Field()
    Fans = scrapy.Field()
    Follower = scrapy.Field()


