import unittest

from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

from org.dove.tissue.CustomWebDriverEventListener import CustomWebDriverEventListener
from org.dove.tissue.WebDriverFactory import WebDriverFactory


class TestTemplate(unittest.TestCase):
    def setUp(self):
        core = WebDriverFactory().create()
        self.driver = EventFiringWebDriver(core, CustomWebDriverEventListener())

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        self.driver.get('https://www.google.com')


if __name__ == '__main__':
    unittest.main()
