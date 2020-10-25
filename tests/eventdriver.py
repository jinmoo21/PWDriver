import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from core import WebDriverFactory
from listener import EventListener
from util import get_logger


logger = get_logger('eventdriver')


class EventDriverTest(unittest.TestCase):
    def setUp(self):
        core1 = WebDriverFactory().launch()
        core2 = WebDriverFactory().launch()
        self.driver1 = EventFiringWebDriver(core1, EventListener())
        self.driver2 = EventFiringWebDriver(core2, EventListener())
        self.driver1.maximize_window()
        self.wait1 = WebDriverWait(self.driver1, 5)
        self.wait2 = WebDriverWait(self.driver2, 5)

    def tearDown(self):
        self.driver2.quit()
        self.driver1.quit()

    def test_something(self):
        self.driver1.get('https://www.google.com')
        logger.info(self.driver1.title)
        self.assertIn(self.driver1.title, 'Google')
        self.driver1.get('https://www.naver.com')
        news_btn1 = self.driver1.find_element(By.CSS_SELECTOR, '.link_news')
        news_btn1.click()
        logger.info(self.driver1.current_url)
        self.assertTrue(self.wait1.until(expected_conditions.url_contains('https://news.naver.com')))

        self.driver2.get('https://www.google.com')
        logger.info(self.driver2.title)
        self.assertIn(self.driver2.title, 'Google')
        self.driver2.get('https://www.naver.com')
        news_btn2 = self.driver2.find_element(By.CSS_SELECTOR, '.link_join')
        news_btn2.click()
        logger.info(self.driver2.current_url)
        self.assertTrue(self.wait2.until(expected_conditions.url_contains('https://nid.naver.com')))


if __name__ == '__main__':
    unittest.main()
