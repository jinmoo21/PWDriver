import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import EventFiringWebDriver

from core import WebDriverFactory
from listener import EventListener
import util

logger = util.get_logger('test')


class TestTemplate(unittest.TestCase):
    def setUp(self):
        core = WebDriverFactory().launch()
        logger.info(f'Browser launched.\nDriver Capabilities: {core.capabilities}')
        self.driver = EventFiringWebDriver(core, EventListener())
        self.driver.maximize_window()

        # self.chrome = WebDriverFactory().setup_chromedriver()
        # self.chrome = WebDriverFactory().setup_geckodriver()
        # self.chrome = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()
        # self.chrome.quit()

    def test_something(self):
        self.driver.get('https://www.google.com')
        self.driver.get('https://www.naver.com')
        print(self.driver.title)
        naver = self.driver.find_element(By.CSS_SELECTOR, '.logo_naver')
        naver.click()
        self.driver.back()
        self.driver.get('https://www.daum.net')
        # self.chrome.get('https://www.daum.net')
        # self.chrome.get('https://www.google.com')
        # self.chrome.back()


if __name__ == '__main__':
    unittest.main()
