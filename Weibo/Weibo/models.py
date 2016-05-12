# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-03-11 17:09:15
# @Last Modified by:   fibears
# @Last Modified time: 2016-05-12 09:21:11

from datetime import datetime
from pony.orm import *

db = Database()


class WeiboEntity(db.Entity):
    """docstring for WeiboEntity"""

    _table_ = 'Content'

    id = PrimaryKey(int, size = 64, unsigned = True, auto = True)
    Name = Optional(str)
    Url = Optional(str)
    uid = Required(str)
    Content = Optional(LongUnicode)
    Repost = Optional(str)
    Comment = Optional(str)
    Like = Optional(str)
    PostTime = Optional(str)

class UserEntity(db.Entity):
    """docstring for UserEntity"""

    _table_ = 'UserInformation'

    id = PrimaryKey(int, size = 64, unsigned = True, auto = True)
    uid = Required(str)
    Name = Optional(str)
    FansNum = Optional(str)
    FollowerNum = Optional(str)
    # Fans = Optional(LongUnicode)
    Follower = Optional(LongUnicode)






