# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    Type = scrapy.Field()
    Name = scrapy.Field()
    ContentId = scrapy.Field()
    Content = scrapy.Field()
    UID = scrapy.Field()
    Repost = scrapy.Field()
    Comment = scrapy.Field()
    Like = scrapy.Field()
    PostTime = scrapy.Field()

class CommentItem(scrapy.Item):
    Type = scrapy.Field()
    Name = scrapy.Field()
    CommentId = scrapy.Field()
    Content = scrapy.Field()
    UID = scrapy.Field()
    PostTime = scrapy.Field()


class UserItem(scrapy.Item):
    UID = scrapy.Field()
    Name = scrapy.Field()
    TweetsNum = scrapy.Field()
    FansNum = scrapy.Field()
    FollowersNum = scrapy.Field()
    # Fans = scrapy.Field()
    CrawlFollowers = scrapy.Field()
    Follower = scrapy.Field()


