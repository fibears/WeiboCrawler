# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-03-11 17:09:15
# @Last Modified by:   zengphil
# @Last Modified time: 2016-05-28 23:22:07

from datetime import datetime
from pony.orm import *

db = Database()


class WeiboEntity(db.Entity):
    """docstring for WeiboEntity"""

    _table_ = 'Content'

    id = PrimaryKey(int, size = 64, unsigned = True, auto = True)
    Type = Optional(str)
    Name = Optional(str)
    ContentId = Optional(str)
    uid = Required(str)
    Content = Optional(LongUnicode)
    Repost = Optional(str)
    Comment = Optional(str)
    Like = Optional(str)
    PostTime = Optional(str)

class CommentEntity(db.Entity):
    """docstring for ContentEntity"""
    _table_ = 'CommentInformation'

    id = PrimaryKey(int, size = 64, unsigned = True, auto = True)
    Type = Optional(str)
    Name = Optional(str)
    CommentId = Optional(str)
    uid = Required(str)
    Content = Optional(LongUnicode)
    PostTime = Optional(str)


class UserEntity(db.Entity):
    """docstring for UserEntity"""

    _table_ = 'UserInformation'

    id = PrimaryKey(int, size = 64, unsigned = True, auto = True)
    uid = Required(str)
    Name = Optional(str)
    TweetsNum = Optional(str)
    FansNum = Optional(str)
    FollowersNum = Optional(str)
    CrawlFollowers = Optional(str)
    # Fans = Optional(LongUnicode)
    Follower = Optional(LongUnicode)






