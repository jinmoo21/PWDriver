import unittest

from selenium import webdriver

from pwdriver import core
from pwdriver import util

logger = util.get_logger('firefox')


class FirefoxTest(unittest.TestCase):
    def setUp(self):
        core.setup_geckodriver()
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        self.driver.get('https://www.google.com')


if __name__ == '__main__':
    unittest.main()
