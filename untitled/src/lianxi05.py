import time

from selenium import webdriver


driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
# assert "Python" in driver.title
driver.find_element_by_id("kw").send_keys('小白')
time.sleep(5)
# elem.find_element_by_id("")
driver.find_element_by_id("su").click()
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
time.sleep(5)
driver.close()