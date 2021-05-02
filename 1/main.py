import os
from selenium import webdriver

os.environ['PATH'] += r"C:/SeleniumDrivers"
driver = webdriver.Chrome()
driver.get("https://www.seleniumeasy.com/test/jquery-download-progress-bar-demo.html")
driver.implicitly_wait(30)
my_element = driver.find_element_by_id('downloadButton')
my_element.click()