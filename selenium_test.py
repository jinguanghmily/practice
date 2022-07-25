#!/usr/bin/env python
# coding=utf-8

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

'''
元素定位的8种方法
id	唯一的
name	元素的名称
class name	元素的类名
tag name	标签，不推荐，重复率太高
link text	文本链接
partial link text	对文本链接的一种补充
xpath	相对/绝对路径
css selector	css定位
'''

'''
页面等待3种方法
time.sleep()
显式等待WebDriverWait().until()方法.WebDriverWait()里填driver和要等待的时间,until或until_not里填等待的元素.
隐式等待driver.implicitly_wait(10)#如果某些元素不是立即可用的,隐式等待是告诉WebDriver去等待一定的时间后去查找元素。
       #默认等待时间是0秒,一旦设置该值,隐式等待是设置该WebDriver的实例的生命周期。
'''
driver = webdriver.Chrome("/Users/jinguang/Downloads/chromedriver")
driver.maximize_window()
#driver.get('https://college.aiimooc.com/')
#driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/a[1]').click()
driver.get('https://www.aiimooc.com/member/login.php?forward=https://college.aiimooc.com/') #登录界面
WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.ID,"username"))) #等待登录界面加载完成
driver.find_element(By.ID,'username').send_keys("17764519401")
driver.find_element(By.ID,'password').send_keys("lily007")
driver.find_element(By.NAME,'submit').click()
driver.get('https://www.aiimooc.com/member/trade.php?action=order') #打开我的订单页面
driver.find_element(By.LINK_TEXT,'多机器人系统路径规划技术与实践').click() #点击其中一个课程，会打开另外一个窗口，对应driver.window_handles[1]
#driver.close()#关闭第一个窗口
driver.switch_to.window(driver.window_handles[1]) #driver.window_handles[0]是第一个窗口

WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="g-main"]/div/div[1]/div[3]/a[1]'))) #等待登录界面加载完成
driver.find_element(By.XPATH,'//*[@id="g-main"]/div/div[1]/div[3]/a[1]').click() #点击进入教室

close_wechat_dailog = WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.XPATH,
'//*[@id="g-main"]/div/div[4]/div/div[1]/button/i')))#弹出的“加入微信群的对话框”
close_wechat_dailog.click()

original_window = driver.current_window_handle
chapters_element = driver.find_elements(By.XPATH,'//*[@id="g-main"]/div/div[2]/div[1]/ul/*') #//*[@id="g-main"]/div/div[2]/div[1]/ul
for chapter in chapters_element:
    lessons_element = chapter.find_elements(By.XPATH,'././ul/*') #//*[@id="g-main"]/div/div[2]/div[1]/ul/li[1]/ul
    for lesson in lessons_element:
        href = lesson.find_element(By.XPATH,'./a').get_attribute('href')
        driver.execute_script(f'window.open("{href}", "_blank");')# 在新的标签页打开链接
        driver.switch_to.window(driver.window_handles[-1])
        video_element = WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="c-study-video-wrapper"]/container/video')))
        course_src = video_element.get_attribute("src")
        print(course_src)
        driver.close()
        # 切回到之前的标签页
        driver.switch_to.window(original_window)


        # lesson.find_element(By.XPATH,'./a/i').click()#点击每一门课程
        #获取课程链接
        # video_element = WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="c-study-video-wrapper"]/container/video')))
        # course_src = video_element.get_attribute("src")
        # print(course_src)
        # driver.back()
        #退回课程列表页面又会弹出加入微信群，关闭微信群对话框
        # close_wechat_dailog = WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.XPATH,
        # '//*[@id="g-main"]/div/div[4]/div/div[1]/button/i')))#弹出的“加入微信群的对话框”
        # close_wechat_dailog.click()
        # time.sleep(5)
driver.quit()