def scroll_into_view_with_js(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


# to be used for testing or debugging
def highlight_element(driver, element):
    driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", element,
                          "style", "border: 2px solid red;")
