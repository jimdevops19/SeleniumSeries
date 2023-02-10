from selenium.webdriver.support.wait import WebDriverWait

from booking.config import Timeout


def get_webdriver_wait(driver, timeout: Timeout) -> WebDriverWait:
    return WebDriverWait(driver, timeout.value)