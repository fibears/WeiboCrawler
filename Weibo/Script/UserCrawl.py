# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-05-12 09:22:41
# @Last Modified by:   fibears
# @Last Modified time: 2016-06-01 10:25:13

import time
import pickle
import random
import re
import numpy as np

from selenium import webdriver
from pony.orm import *

SQLDB = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'mysqlpasswd',
    'db': 'Weibo'
}

Newdb = Database()

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
    Newdb.bind('mysql', **SQLDB)
    Newdb.generate_mapping()
    with db_session:
        Person = select(p for p in UserEntity)
        person = [p for p in Person if int(p.CrawlFollower) <= int(p.FollowerNum)/2]
        UserURL = ['http://m.weibo.cn/u/' + p.uid for p in person]
        FollowerNum = [p.FollowerNum for p in person]
        print "Get UserUID Finish!( Num:%d)" % len(UserURL)
    return UserURL, FollowerNum

SQL_UserURL, SQL_FollowerNum = getUsersData()

# Crawl UserInformationData #

driver = webdriver.PhantomJS()
url = "http://m.weibo.cn/u/1984250112"
driver.get(url)
with open("cookie.txt", "r") as f:
    cookieweibo = pickle.load(f)
for cookie in cookieweibo:
    driver.add_cookie(cookie)

pattern = re.compile(r'http://m.weibo.cn/u/(\d{10})')
for i in range(0, len(SQL_UserURL)):
    try:
        UserUrl = SQL_UserURL[i]
        FollowerNum = SQL_FollowerNum[i]
        driver.get(UserUrl)
        print 'Get UserUrl: %s' % UserUrl
        time.sleep(np.random.choice(range(4,8)))
        FollowerUrl = driver.find_element_by_xpath("//a[contains(@href, 'FOLLOWERS')]").get_attribute('href')
        driver.get(FollowerUrl)
       # time.sleep(np.random.choice(range(4,8)))
        for i in xrange(1,(np.int(FollowerNum)/10 + 4)):
            print 'Get Followers: Page %d' % i
            time.sleep(np.random.choice(range(8,15)))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        Users = driver.find_elements_by_xpath("//div[@class='layout-box media-graphic']/a[1]")
        UserList = []
        for user in Users:
            if re.findall(pattern, user.get_attribute('href')) != []:
                UserList.append(re.findall(pattern, user.get_attribute('href'))[0])
        CrawlFollower = str(len(UserList))
        Follower = '.'.join(UserList)

        # database #
        item_uid = re.findall(pattern, UserUrl)[0]
        if int(CrawlFollower) >= int(FollowerNum)/2:
            with db_session:
                userEntity = UserEntity.get(uid = item_uid)
                userEntity.CrawlFollower = CrawlFollower
                userEntity.Follower = Follower
                print("User'uid is : ", item_uid)
                print('save post')
    except Exception:
        pass


driver.quit()




