from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support import expected_conditions as EC

from booking.filtration import Filtration
import booking.constants as const
from booking.helpers import get_webdriver_wait
from booking.report import Report
from prettytable import PrettyTable

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

    def apply_filtrations(self):
        filtration = Filtration(driver=self)
        filtration.apply_star_rating(4, 5)

        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_elements(By.XPATH, "//div[@data-testid='property-card']")

        report = Report(self, hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)
