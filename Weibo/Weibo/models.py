# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-03-11 17:09:15
# @Last Modified by:   zengphil
# @Last Modified time: 2016-05-05 17:31:01

from datetime import datetime
from pony.orm import *

db = Database()


class WeiboEntity(db.Entity):
    """docstring for EstateEntity"""

    _table_ = 'Weibo'

    id = PrimaryKey(int, size = 64, unsigned = True, auto = True)
    uid = Required(str)
    # webstie = Optional(str)
    Content = Optional(LongUnicode)
    Respost = Optional(int, size = 32)
    Comment = Optional(int, size = 32)
    Like = Optional(int, size = 32)
    PostTime = Optional(datetime)

class UserEntity(db.Entity):
    """docstring for UserEntity"""

    _table_ = 'UserInformation'

    id = PrimaryKey(int, size = 64, unsigned = True, auto = True)
    uid = Required(str)
    Name = Optional(str)
    FansNum = Optional(str)
    FollowerNum = Optional(str)
    Fans = Optional(LongUnicode)
    Follower = Optional(LongUnicode)






