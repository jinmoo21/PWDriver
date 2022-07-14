from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from pages.bing_page import BingPage
from pwdriver.core import WebDriverFactory
from pwdriver.listener import EventListener

import unittest


class BrowserTest(unittest.TestCase):
    def setUp(self):
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = EventFiringWebDriver(WebDriverFactory().launch(options=options), EventListener())

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        page = BingPage(self.driver)
        page.get()
        page.type_keyword("치킨")
        page.click_search()
        self.assertIn("https://www.bing.com/search?q=%EC%B9%98%ED%82%A8", self.driver.current_url)
        self.assertEqual("치킨 - Search", self.driver.title)
