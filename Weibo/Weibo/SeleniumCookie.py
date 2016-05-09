#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: fibears
# @Date:   2016-05-05 20:55:26
# @Last Modified by:   fibears
# @Last Modified time: 2016-05-09 13:42:00

import time
from selenium import webdriver
import pickle

URL = "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F"

# TO GET COOKIE FOR SELENIUM WEBDRIVER
driver = webdriver.PhantomJS()
driver.get(URL)
time.sleep(3)
User = driver.find_element_by_xpath("//p[@class='input-box']/input[@type='text']")
User.send_keys('xxxx')
PassWord = driver.find_element_by_xpath("//p[@class='input-box']/input[@type='password']")
PassWord.send_keys('xxxx')
driver.find_element_by_xpath("//a[@id='loginAction']").click()

cookie = driver.get_cookies()
with open('cookie.txt', 'w') as f:
    pickle.dump(cookie, f)
