import unittest

from selenium import webdriver

from pwdriver import util

logger = util.get_logger('safari')


class SafariTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Safari()
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        self.driver.get('https://www.google.com')


if __name__ == '__main__':
    unittest.main()
