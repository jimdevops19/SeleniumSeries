from selenium.webdriver.support.wait import WebDriverWait

from booking.config import Timeout


def get_webdriver_wait(driver, timeout: Timeout) -> WebDriverWait:
    return WebDriverWait(driver, timeout.value)


def scroll_into_view_with_js(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def highlight_element(driver, element):
    original_style = element.get_attribute("style")
    driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])",
                          element,
                          "style",
                          "border: 2px solid red;")
