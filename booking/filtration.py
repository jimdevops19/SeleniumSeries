# This file will include a class with instance methods.
# That will be responsible to interact with our website
# After we have some results, to apply filtrations.
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.support import expected_conditions as EC

from booking.helpers import scroll_into_view_with_js, get_webdriver_wait
from config import Timeout


class Filtration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        star_filtration_box = self.driver.find_element(By.XPATH, "//div[contains(@id, 'filter_group_class')]")
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, '*')

        # todo optimize this loop maybe
        for star_value in star_values:

            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    scroll_into_view_with_js(self.driver, star_element)
                    star_element.click()

    def sort_price_lowest_first(self):
        sort_by_element = self.driver.find_element(By.XPATH, "//button[@data-testid='sorters-dropdown-trigger']")
        sort_by_element.click()
        lowest_price_locator = (By.XPATH, "//span[contains(text(), 'Price') and contains(text(), 'lowest')]")
        lowest_price_element = get_webdriver_wait(self.driver, Timeout.MEDIUM).until(
            EC.element_to_be_clickable(lowest_price_locator))
        lowest_price_element.click()
