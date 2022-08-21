import unittest

from appium.webdriver.common.appiumby import AppiumBy

from pwdriver.core import WebDriverFactory


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = WebDriverFactory().launch()

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        self.driver.get('https://google.com')
        self.assertIn(self.driver.title, 'Google')
        self.driver.get('https://m.naver.com')
        news_btn1 = self.driver.find_element(by=AppiumBy.CSS_SELECTOR, value="a[data-clk='shortcafe']")
        news_btn1.click()
        self.assertTrue(self.driver.current_url.startswith('https://m.cafe.naver.com'))


if __name__ == '__main__':
    unittest.main()
