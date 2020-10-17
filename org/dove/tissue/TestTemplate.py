import unittest

from selenium.webdriver.support.events import EventFiringWebDriver

from org.dove.tissue.CustomWebDriverEventListener import CustomWebDriverEventListener
from org.dove.tissue.WebDriverFactory import WebDriverFactory


class TestTemplate(unittest.TestCase):
    def setUp(self):
        core = WebDriverFactory().launch()
        self.driver = EventFiringWebDriver(core, CustomWebDriverEventListener()).wrapped_driver
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        self.driver.get('https://www.google.com')
        self.driver.get('https://www.naver.com')
        print(self.driver.title)

if __name__ == '__main__':
    unittest.main()
