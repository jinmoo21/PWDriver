from selenium.webdriver.common.by import By

from pwdriver.page import BasePage


class BingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self._url = 'https://www.bing.com'
        self._locator = {
            'input': (By.CSS_SELECTOR, 'input#sb_form_q'),
            'search': (By.CSS_SELECTOR, 'label#search_icon')
        }

    def type_keyword(self, text) -> None:
        self._by('input').send_keys(text)

    def click_search(self) -> BasePage:
        self._by('search').click()
        return BingPage(BasePage)
