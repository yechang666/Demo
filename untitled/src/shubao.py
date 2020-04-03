#coding=utf-8
from appium import webdriver
import time
import random

desired_caps = {
    "platformName" : "Android",
    "platformVersion": "7.0",
    "deviceName": "dce1681a0104",
    "noReset": "true",
    "appPackage": "com.jm.video",
    "appActivity": ".ui.main.SplashActivity"
}

dr = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
x = dr.get_window_size()['width']
y = dr.get_window_size()['height']
time.sleep(2)
while True:
    # time.sleep(2)
    dr.swipe(int(x * 0.5),int(y * 0.65), int(x * 0.5), int(y * 0.25))
    m = random.randint(10,30)
    # print(m)
    time.sleep(m)



# dr.quit()