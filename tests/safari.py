import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pwdriver import util
from pwdriver.val import OS_NAME

logger = util.get_logger('safari')


@unittest.skipIf(OS_NAME != 'MAC', 'Safari only runs on MacOSX.')
class SafariTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Safari()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        self.driver.get('https://www.google.com')
        self.wait.until(expected_conditions.title_contains('Google'))
        logger.info(self.driver.title)
        self.assertIn(self.driver.title, 'Google')
        self.driver.get('https://www.naver.com')
        news_btn1 = self.driver.find_element(By.CSS_SELECTOR, '.link_news')
        news_btn1.click()
        self.wait.until(expected_conditions.url_contains('https://news.naver.com'))
        logger.info(self.driver.current_url)
        self.assertIn('https://news.naver.com', self.driver.current_url)

        self.driver.get('https://www.google.com')
        self.wait.until(expected_conditions.title_contains('Google'))
        logger.info(self.driver.title)
        self.assertIn(self.driver.title, 'Google')
        self.driver.get('https://www.naver.com')
        news_btn2 = self.driver.find_element(By.CSS_SELECTOR, '.link_join')
        news_btn2.click()
        self.wait.until(expected_conditions.url_contains('https://nid.naver.com'))
        logger.info(self.driver.current_url)
        self.assertIn('https://nid.naver.com', self.driver.current_url)


if __name__ == '__main__':
    unittest.main()
