from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support import expected_conditions as EC

from booking.filtration import Filtration
import booking.constants as const
from booking.helpers import get_webdriver_wait, scroll_into_view_with_js

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from config import Timeout


class Booking(webdriver.Chrome):
    # todo specify input or manual config
    def __init__(self, teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options, service=ChromeService(ChromeDriverManager().install()))
        # self.implicitly_wait(10)

    def accept_cookies(self):
        self.find_element(By.ID, 'onetrust-accept-btn-handler').click()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-tooltip-text="Choose your currency"]')
        currency_element.click()

        selected_currency_element = self.find_element(
            By.CSS_SELECTOR, f'a[data-modal-header-async-url-param*="selected_currency={currency}"]')
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.NAME, 'ss')
        search_field.click()
        search_field.clear()

        results_list_locator = (By.XPATH, "//ul")
        popular_destinations_locator = (By.XPATH, "//span[contains(text(), 'Popular destinations nearby')]")
        search_field.send_keys(place_to_go)
        # search_field.click()
        get_webdriver_wait(self, Timeout.MEDIUM).until(EC.visibility_of_element_located(results_list_locator))
        get_webdriver_wait(self, Timeout.MEDIUM).until(EC.invisibility_of_element_located(popular_destinations_locator))

        first_result_locator = locate_with(By.XPATH, "//li[1]").below({By.NAME: 'ss'})
        self.find_element(first_result_locator).click()

    def select_dates(self, check_in_date, check_out_date):
        # accommodation_element = self.find_element(By.ID, "accommodation")
        # accommodation_element.click()
        check_in_date_element = get_webdriver_wait(self, Timeout.MEDIUM).until(
            EC.visibility_of_element_located((By.XPATH, f'//*[@data-date="{check_in_date}"]')))
        check_in_date_element.click()

        check_out_element = self.find_element(By.XPATH, f'//*[@data-date="{check_out_date}"]')
        check_out_element.click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    def apply_star_rating(self, *star_values):
        star_filtration_box = self.find_element(By.XPATH, "//div[contains(@id, 'filter_group_class')]")
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, '*')

        # todo optimize this loop maybe
        for star_value in star_values:

            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    scroll_into_view_with_js(self, star_element)
                    star_element.click()

    def sort_price_lowest_first(self):
        sort_by_element = self.find_element(By.XPATH, "//button[@data-testid='sorters-dropdown-trigger']")
        sort_by_element.click()
        lowest_price_locator = (By.XPATH, "//span[contains(text(), 'Price') and contains(text(), 'lowest')]")
        lowest_price_element = get_webdriver_wait(self, Timeout.MEDIUM).until(
            EC.element_to_be_clickable(lowest_price_locator))
        lowest_price_element.click()

    def extract_results(self) -> list[list[str]]:
        deal_boxes = self.find_elements(By.XPATH, "//div[@data-testid='property-card']")

        results = []
        for deal_box in deal_boxes:
            hotel_name = deal_box.find_element(By.XPATH, ".//*[@data-testid='title']").text
            hotel_price = deal_box.find_element(By.XPATH, ".//*[@data-testid='price-and-discounted-price']").text
            try:
                hotel_score = deal_box.find_element(By.XPATH, ".//*[@data-testid='review-score']/div").text
            except NoSuchElementException:
                hotel_score = 'new'
            results.append([hotel_name, hotel_price, hotel_score])
        return results
