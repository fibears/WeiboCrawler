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
from Weibo.models import CommentEntity

from items import WeiboItem, UserItem, CommentItem

settings = get_project_settings()

class WeiboPipeline(object):

    def __init__(self):
        db.bind('mysql', **settings.get('SQLDB'))
        db.generate_mapping()

    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            try:
                item_Contentid = item['ContentId']

                with db_session:
                    weiboEntity = WeiboEntity.get(ContentId = item_Contentid)

                    if weiboEntity:
                        print('already have this Content item')
                        return

                    weiboEntity = WeiboEntity(
                        ContentId = item_Contentid,
                        Type = item['Type'],
                        Name = item['Name'],
                        uid = item['UID'],
                        Content = item['Content'],
                        Repost = item['Repost'],
                        Comment = item['Comment'],
                        Like = item['Like'],
                        PostTime = item['PostTime']
                    )

                    print('ContentId: ', item_Contentid)
                    print('save post')

            except Exception:
                print "What are you doing?"

        if isinstance(item, CommentItem):
            try:
                item_Commentid = item['CommentId']

                with db_session:
                    commentEntity = CommentEntity.get(CommentId = item_Commentid)

                    if commentEntity:
                        print('already have this url item')
                        return

                    commentEntity = CommentEntity(
                        CommentId = item_Commentid,
                        Type = item['Type'],
                        Name = item['Name'],
                        uid = item['UID'],
                        Content = item['Content'],
                        PostTime = item['PostTime']
                    )

                    print('CommentId: ', item_Commentid)
                    print('save post')

            except Exception:
                print "What are you doing?"

        if isinstance(item, UserItem):
            try:
                item_Useruid = item['UID']

                with db_session:
                    userEntity = UserEntity.get(uid = item_Useruid)
                    if userEntity:
                        print('already have this uid item')
                        return

                    userEntity = UserEntity(
                        uid = item['UID'],
                        Name = item['Name'],
                        TweetsNum = item['TweetsNum'],
                        FansNum = item['FansNum'],
                        FollowersNum = item['FollowersNum'],
                        CrawlFollowers = item['CrawlFollowers'],
                        Follower = item['Follower']
                    )

                    print("User'uid is : ", item_Useruid)
                    print('save post')

            except Exception:
                print "What are you doing?"
        return item


    def close_spider(self, spider):
        db.disconnect()
