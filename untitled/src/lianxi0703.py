#coding=utf-8
from datetime import datetime
import  time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://www.baidu.com/")
driver.maximize_window()
# time.sleep(2)
# driver.find_element_by_link_text('地图').click()
# driver.find_element_by_id("kw").send_keys("美女")
# driver.find_element_by_id("su").click()
#driver.findElement(By.xpath('//*[@id="form"]/span[contains(@class,"bg s_ipt_wr")]/input'))

#driver.find_element_by_xpath('//*[@id="form"]/child::span[@class="bg s_btn_wr"]')
#driver.find_element_by_xpath('//*[@id="form"]/span[@class="bg s_btn_wr"]')
start = datetime.now()
wait = WebDriverWait(driver, 30)
dd = wait.until(lambda x: x.find_element_by_xpath('//span[@class="bg s_ipt_wr quickdelete-wrap"]/input'))
dd.send_keys("Python")
end = datetime.now()
# driver.find_element_by_xpath('//span[contains(@class,"bg s_ipt_wr quickdelete-wrap")]')
# driver.find_element_by_xpath('//span[@class="bg s_ipt_wr quickdelete-wrap"]/input').send_keys("Python")
print((end-start).seconds)






