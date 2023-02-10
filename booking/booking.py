from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

from booking.filtration import Filtration
import booking.constants as const
from booking.report import Report
from prettytable import PrettyTable

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class Booking(webdriver.Chrome):
    def __init__(self, teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options, service=ChromeService(ChromeDriverManager().install()))
        # self.implicitly_wait(10)

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
        # todo explicit wait here
        search_field = self.find_element(By.NAME, 'ss')
        search_field.click()
        search_field.clear()
        search_field.send_keys(place_to_go)

        # todo this dict seems weird
        first_result_locator = locate_with(By.XPATH, "//li[1]").below({By.NAME: 'ss'})
        first_result = self.find_element(first_result_locator)
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_date_element = self.find_element(By.XPATH, f'//span[@data-date="{check_in_date}"]')
        check_in_date_element.click()

        check_out_element = self.find_element(By.XPATH, f'//span[@data-date="{check_out_date}"]')
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.find_element(By.ID, 'xp__guests__toggle')
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element(
                By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]')
            decrease_adults_element.click()
            # If the value of adults reaches 1, then we should get out
            # of the while loop
            adults_value_element = self.find_element(By.ID, 'group_adults')
            adults_value = adults_value_element.get_attribute(
                'value'
            )  # Should give back the adults count

            if int(adults_value) == 1:
                break

        increase_button_element = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]')

        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    def apply_filtrations(self):
        filtration = Filtration(driver=self)
        filtration.apply_star_rating(4, 5)

        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_element(By.ID, 'hotellist_inner')

        report = Report(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)
