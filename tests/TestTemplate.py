import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import EventFiringWebDriver

import Logger
from EventListener import EventListener
from WebDriverFactory import WebDriverFactory

logger = Logger.get_logger('test')


class TestTemplate(unittest.TestCase):
    def setUp(self):
        core = WebDriverFactory().launch()
        logger.info(f'Browser launched.\nDriver Capabilities: {core.capabilities}')
        self.driver = EventFiringWebDriver(core, EventListener())
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        self.driver.get('https://www.google.com')
        self.driver.get('https://www.naver.com')
        print(self.driver.title)
        naver = self.driver.find_element(By.CSS_SELECTOR, '.logo_naver')
        naver.click()
        self.driver.back()


if __name__ == '__main__':
    unittest.main()
