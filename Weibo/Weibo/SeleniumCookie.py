#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-05-05 20:55:26
# @Last Modified by:   fibears
# @Last Modified time: 2016-05-12 21:00:12

import time
import pickle
import random

from selenium import webdriver

WeiBoAccount = [
    {'no': 'xxx@qq.com', 'psw': 'xxx'},
    {'no': 'xxx@sina.com', 'psw': 'xxx'},
]

URL = "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F"

# TO GET COOKIE FOR SELENIUM WEBDRIVER
driver = webdriver.PhantomJS()
driver.get(URL)
time.sleep(3)
Account = random.choice(WeiBoAccount)
User = driver.find_element_by_xpath("//p[@class='input-box']/input[@type='text']")
User.send_keys(Account['no'])
PassWord = driver.find_element_by_xpath("//p[@class='input-box']/input[@type='password']")
PassWord.send_keys(Account['psw'])
driver.find_element_by_xpath("//a[@id='loginAction']").click()

cookie = driver.get_cookies()
with open('cookie.txt', 'w') as f:
    pickle.dump(cookie, f)
driver.quit()
