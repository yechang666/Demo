from selenium import webdriver
import time

brower = webdriver.Chrome()
brower.get("http://www.baidu.com")

# brower.find_element_by_id('kw').send_keys('selenium')
brower.find_element_by_name("tj_trmap").click()
# brower.find_element_by_id('su').click()
brower.find_element_by_id('sole-input').send_keys('天通苑')
brower.find_element_by_id("search-button").click()

time.sleep(3)
brower.close()
