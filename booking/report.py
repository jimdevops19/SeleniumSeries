# This file is going to include method that will parse
# The specific data that we need from each one of the deal boxes.
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from booking.helpers import highlight_element


class Report:
    def __init__(self, driver, deal_boxes: list[WebElement]):
        self.deal_boxes = deal_boxes
        self.driver = driver

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find_element(By.XPATH, ".//*[@data-testid='title']").text
            hotel_price = deal_box.find_element(By.XPATH, ".//*[@data-testid='price-and-discounted-price']").text
            try:
                hotel_score = deal_box.find_element(By.XPATH, ".//*[@data-testid='review-score']/div").text
            except NoSuchElementException:
                hotel_score = 'new'
            collection.append([hotel_name, hotel_price, hotel_score])
        return collection
