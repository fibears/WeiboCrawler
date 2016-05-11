# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pony.orm import db_session

from scrapy.utils.project import get_project_settings

from Weibo.models import db
from Weibo.models import WeiboEntity
from Weibo.models import UserEntity

from items import WeiboItem, UserItem

settings = get_project_settings()

class WeiboPipeline(object):

    def __init__(self):
        db.bind('mysql', **settings.get('SQLDB'))
        db.generate_mapping()

    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            try:
                item_url = item['Url']

                with db_session:
                    weiboEntity = WeiboEntity.get(Url = item_url)

                    if weiboEntity:
                        print('already have this url item')
                        return

                    weiboEntity = WeiboEntity(
                        Url = item_url,
                        uid = item['UID'],
                        Content = item['Content'],
                        Repost = item['Repost'],
                        Comment = item['Comment'],
                        Like = item['Like'],
                        PostTime = item['PostTime']
                    )

                    print('url: ', item_url)
                    print('save post')

            except Exception:
                pass

        if isinstance(item, UserItem):
            try:
                item_uid = item['UID']

                with db_session:
                    userEntity = UserEntity.get(uid = item_uid)

                    if userEntity:
                        print('already have this uid item')
                        return

                    userEntity = UserEntity(
                        uid = item['UID'],
                        Name = item['Name'],
                        FansNum = item['FansNum'],
                        FollowerNum = item['FollowerNum'],
                        # Fans = item['Fans'],
                        Follower = item['Follower']
                    )

                    print("User'uid is : ", item_uid)
                    print('save post')

            except Exception:
                pass


    def close_spider(self, spider):
        db.disconnect()
