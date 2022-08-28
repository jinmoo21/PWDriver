import unittest

from selenium.webdriver.support.events import EventFiringWebDriver

from pwdriver.core import WebDriverFactory
from pwdriver.listener import EventListener
from pwdriver.util import get_logger
from tests.pages.bing_page import BingPage

logger = get_logger('test')


class EventDriverTest(unittest.TestCase):
    def setUp(self):
        core = WebDriverFactory.launch()
        self.driver = EventFiringWebDriver(core, EventListener())
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        page = BingPage(self.driver)
        page.jquery = False
        page.angular = False
        page.get()
        page.wait_until_fully_loaded()
        keyword = 'chicken'
        page.type_keyword(keyword)
        page.click_search()
        page.wait_until_fully_loaded()
        self.assertIn(f'https://www.bing.com/search?q={keyword}', self.driver.current_url)
        self.assertEqual(f'{keyword} - Search', self.driver.title)
        self.driver.back()
        page.wait_until_fully_loaded()
        self.assertIn('https://www.bing.com', self.driver.current_url)
        self.driver.forward()
        page.wait_until_fully_loaded()
        self.assertIn(f'https://www.bing.com/search?q={keyword}', self.driver.current_url)


if __name__ == '__main__':
    unittest.main()
