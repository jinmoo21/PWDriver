from pwdriver.core import WebDriverFactory
from tests.pages.bing_page import BingPage

import unittest


class BrowserTest(unittest.TestCase):
    def setUp(self):
        self.driver = WebDriverFactory().launch()

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        page = BingPage(self.driver)
        page.get()
        page.type_keyword("치킨")
        page.click_search()
        self.assertIn("https://www.bing.com/search?q=%EC%B9%98%ED%82%A8", self.driver.current_url)
        self.assertEqual("치킨 - Search", self.driver.title)


if __name__ == '__main__':
    unittest.main()
