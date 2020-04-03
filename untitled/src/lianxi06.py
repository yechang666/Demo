#coding=utf-8
from appium import webdriver

desired_caps = {
    "platformName" : "Android",
    "platformVersion": "7.0",
    "deviceName": "dce1681a0104",
    "noReset": "true",
    "appPackage": "ej.easyjoy.multicalculator.cn",
    "appActivity": "ej.easyjoy.cal.activity.LogoActivity"
}

dr = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

dr.find_element_by_id("ej.easyjoy.multicalculator.cn:id/seven").click()
dr.find_element_by_id("ej.easyjoy.multicalculator.cn:id/add").click()
dr.find_element_by_id("ej.easyjoy.multicalculator.cn:id/one").click()
dr.find_element_by_id("ej.easyjoy.multicalculator.cn:id/equal").click()


dr.quit()