import unittest

from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pwdriver.core import WebDriverFactory
from pwdriver.listener import EventListener
from pwdriver.util import get_logger
from tests.pages.bing_page import BingPage

logger = get_logger('eventdriver')


class EventDriverTest(unittest.TestCase):
    def setUp(self):
        core = WebDriverFactory().launch()
        self.driver = EventFiringWebDriver(core, EventListener())
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        page = BingPage(self.driver)
        page.get()
        keyword = 'chicken'
        page.type_keyword(keyword)
        page.click_search()
        self.wait.until(expected_conditions.url_contains('/search?q='))
        self.assertIn(f'https://www.bing.com/search?q={keyword}', self.driver.current_url)
        self.assertEqual(f'{keyword} - Search', self.driver.title)
        self.driver.back()
        self.wait.until(expected_conditions.url_contains('https://www.bing.com'))
        self.assertIn('https://www.bing.com', self.driver.current_url)
        self.driver.forward()
        self.wait.until(expected_conditions.url_contains(f'/search?q={keyword}'))
        self.assertIn(f'https://www.bing.com/search?q={keyword}', self.driver.current_url)
        self.driver.execute_script('window.scrollTo(0, 0)')


if __name__ == '__main__':
    unittest.main()
