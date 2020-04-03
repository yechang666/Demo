# import random
# import time
from appium import webdriver


desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.0'
desired_caps['deviceName'] = 'dce1681a0104'
desired_caps['appPackage'] = 'com.sqage.Ogre.OgreInstance.uc'
desired_caps['noReset'] = 'true'    #appium --no-reset 和这段代码的功能一样
desired_caps['appActivity'] = 'cn.uc.gamesdk.activity.PullupActivity'  #com.sqage.Ogre.OgreInstance.uc/cn.uc.gamesdk.activity.PullupActivity

dr = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# time.sleep(10)  #休眠可以防止出现开机悬浮窗找不到元素的情况
# a = random
# print(a)


# dr.find_element_by_id('com.miui.calculator:id/btn_1_s').click()
# dr.find_element_by_id('com.miui.calculator:id/btn_plus_s').click()
# dr.find_element_by_id('com.miui.calculator:id/btn_3_s').click()
# dr.find_element_by_id('com.miui.calculator:id/btn_equal_s').click()
# dr.quit()