import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pwdriver.core import WebDriverFactory
from pwdriver.listener import EventListener
from pwdriver.util import get_logger
from tests.pages.bing_page import BingPage

logger = get_logger('eventdriver')


class EventDriverTest(unittest.TestCase):
    def setUp(self):
        core = WebDriverFactory().launch()
        self.driver = EventFiringWebDriver(core, EventListener())
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

    def tearDown(self):
        self.driver.quit()

    def test_one(self):
        self.driver.get('https://www.google.com')
        logger.info(self.driver.title)
        self.assertIn(self.driver.title, 'Google')
        self.driver.get('https://www.naver.com')
        news_btn1 = self.driver.find_element(By.CSS_SELECTOR, '.link_news')
        news_btn1.click()
        self.wait.until(expected_conditions.url_contains('https://news.naver.com'))
        logger.info(self.driver.current_url)
        self.assertIn('https://news.naver.com', self.driver.current_url)
        self.driver.back()
        self.assertIn('https://www.naver.com', self.driver.current_url)
        self.driver.forward()
        self.assertIn('https://news.naver.com', self.driver.current_url)

        self.driver.get('https://www.naver.com')
        news_btn2 = self.driver.find_element(By.CSS_SELECTOR, '.link_join')
        news_btn2.click()
        self.wait.until(expected_conditions.url_contains('https://nid.naver.com'))
        logger.info(self.driver.current_url)
        self.assertIn('https://nid.naver.com', self.driver.current_url)
        self.driver.execute_script('window.scrollTo(0, 0)')

    def test_two(self):
        page = BingPage(self.driver)
        page.get()
        page.type_keyword('치킨')
        page.click_search()
        self.wait.until(expected_conditions.url_contains('/search?q='))
        self.assertIn('https://www.bing.com/search?q=%EC%B9%98%ED%82%A8', self.driver.current_url)
        self.assertEqual('치킨 - Search', self.driver.title)


if __name__ == '__main__':
    unittest.main()
