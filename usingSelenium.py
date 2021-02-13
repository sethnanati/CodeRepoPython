from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Safari()
browser.get("https://wiki.ubuntu.com")
element = browser.find_element(By.ID, "searchinput")
element.send_keys("titoluwa")
print(element)
#html = browser.page_source
time.sleep(2)
#print(html)

browser.close
