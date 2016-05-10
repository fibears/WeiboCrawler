# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pony.orm import db_session

from scrapy.utils.project import get_project_settings

from Weibo.models import db
from Weibo.models import WeiboEntity
# from Weibo.models import UserEntity

settings = get_project_settings()

class WeiboPipeline(object):

    def __init__(self):
        db.bind('mysql', **settings.get('SQLDB'))
        db.generate_mapping()

    def process_item(self, weiboItem, spider):
        item_url = weiboItem['Url']

        with db_session:
            weiboEntity = WeiboEntity.get(Url = item_url)

            if weiboEntity:
                print('already have this url item')
                return

            weiboEntity = WeiboEntity(
                Url = item_url,
                uid = weiboItem['UID'],
                Content = weiboItem['Content'],
                Repost = weiboItem['Repost'],
                Comment = weiboItem['Comment'],
                Like = weiboItem['Like'],
                PostTime = weiboItem['PostTime']
            )

            print('url: ', item_url)
            print('save post')

        def spider_closed(self, spider):
            db.disconnect()
