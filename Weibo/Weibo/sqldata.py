# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-05-12 09:22:41
# @Last Modified by:   fibears
# @Last Modified time: 2016-05-21 11:55:38

from pony.orm import *

SQLDB = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'mysqlpasswd',
    'db': 'Weibo'
}

Newdb = Database()

class WeiboEntity(Newdb.Entity):
    """docstring for WeiboEntity"""

    _table_ = 'Content'

    id = PrimaryKey(int, size = 64, unsigned = True, auto = True)
    Type = Optional(str)
    Name = Optional(str)
    Url = Optional(str)
    uid = Required(str)
    Content = Optional(LongUnicode)
    Repost = Optional(str)
    Comment = Optional(str)
    Like = Optional(str)
    PostTime = Optional(str)

class UserEntity(Newdb.Entity):
    """docstring for UserEntity"""

    _table_ = 'UserInformation'

    id = PrimaryKey(int, size = 64, unsigned = True, auto = True)
    uid = Required(str)
    Name = Optional(str)
    FansNum = Optional(str)
    FollowerNum = Optional(str)
    CrawlFollower = Optional(str)
    # Fans = Optional(LongUnicode)
    Follower = Optional(LongUnicode)

def getUsersData():
    """获取数据库中已保存的数据"""

    with db_session:
        Person = select(p for p in UserEntity)
        UserUID = [p.uid for p in Person]
        print "Get UserUID Finish!( Num:%d)" % len(UserUID)
    return UserUID

def getContentData():
    """获取Content数据"""
    """连接数据库"""
    Newdb.bind('mysql', **SQLDB)
    Newdb.generate_mapping()
    with db_session:
        Content = select(p for p in WeiboEntity)
        Content_Url = [p.Url for p in Content]
        print "Get ContentUrl Finish!( Num:%d)" % len(Content_Url)
    return Content_Url

SQL_ContentUrl = getContentData()

SQL_UserUID = getUsersData()
