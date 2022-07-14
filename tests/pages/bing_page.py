from selenium.webdriver.common.by import By

from pwdriver.page import BasePage


class BingPage(BasePage):
    _url = "https://www.bing.com"
    _locator = {
        "input": (By.CSS_SELECTOR, "input#sb_form_q"),
        "search": (By.CSS_SELECTOR, "label#search_icon")
    }

    def __init__(self, driver):
        super().__init__(driver)

    def type_keyword(self, text):
        self._target.element = self._locator["input"]
        self._target.element.send_keys(text)

    def click_search(self):
        self._target.element = self._locator["search"]
        self._target.element.click()
