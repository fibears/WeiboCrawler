# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-05-04 18:40:00
# @Last Modified by:   fibears
# @Last Modified time: 2016-05-09 13:48:14

import urllib
import urllib2
import cookielib
from lxml.html import parse
import lxml

# 设置保存cookie的文件
firename = 'cookieweibo.txt'
# 创建MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(firename)
# 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

url = 'https://passport.weibo.cn/sso/login'

PostData = urllib.urlencode({
    'username': 'xxxx@qq.com',
    'password': 'xxxx'
})

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0)',
    'Host': 'passport.weibo.cn',
    'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F'
}

Request = urllib2.Request(url, PostData, headers)
Response = opener.open(Request)
cookie.save(ignore_discard=True, ignore_expires=True)

##########
#创建MozillaCookieJar实例对象
cookie = cookielib.MozillaCookieJar()
#从文件中读取cookie内容到变量
cookie.load('cookieweibo.txt', ignore_discard=True, ignore_expires=True)
#利用urllib2的build_opener方法创建一个opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

WeiboUrl = 'http://m.weibo.cn/u/1984250112'

Headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0)',
    'Host': 'm.weibo.cn',
    'Referer': 'http://m.weibo.cn/'
}

Result = opener.open(urllib2.Request(WeiboUrl, headers = Headers))
parsed = parse(Result)
cookie.save(filename = 'cookieweibo.txt',ignore_discard=True, ignore_expires=True)


# # Selenium Test
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# browser = webdriver.Chrome()
# browser.get("http://m.webo.cn")

# input = browser.find_element_by_xpath("//a[@class='']")
# input.send_keys(Keys.PAGE_DOWN)
# myhtml = browser.page_source

# # Now set the cookie. This one's valid for the entire domain
# cookie = {‘name’ : ‘foo’, ‘value’ : ‘bar’}
# driver.add_cookie(cookie)

# # And now output all the available cookies for the current URL
# driver.get_cookies()
