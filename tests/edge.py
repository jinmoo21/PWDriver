import unittest

from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from core import WebDriverFactory
from val import OS_NAME, MAC
import util

logger = util.get_logger('edge')


class EdgeTest(unittest.TestCase):
    def setUp(self):
        WebDriverFactory().setup_edgedriver()
        options = EdgeOptions()
        options.use_chromium = True
        options.set_capability('platform', 'MAC' if OS_NAME == MAC else 'WINDOWS')
        self.driver1 = Edge(options=options)
        self.driver2 = Edge(options=options)
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
