import os
from selenium import webdriver
from selenium.webdriver.common.by import By

os.environ['PATH'] += r"C:/SeleniumDrivers"
driver = webdriver.Chrome()
driver.get("https://www.seleniumeasy.com/test/jquery-download-progress-bar-demo.html")
driver.implicitly_wait(30)
my_element = driver.find_element(By.ID, 'downloadButton')
my_element.click()