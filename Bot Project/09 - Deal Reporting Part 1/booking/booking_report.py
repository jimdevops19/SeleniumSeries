# This file is going to include method that will parse
# The specific data that we need from each one of the deal boxes.
from selenium.webdriver.remote.webelement import WebElement


class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements_by_class_name(
            'sr_property_block'
        )

    def pull_titles(self):
        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find_element_by_class_name(
                'sr-hotel__name'
            ).get_attribute('innerHTML').strip()
            print(hotel_name)