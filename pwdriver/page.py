from selenium.webdriver.support.wait import WebDriverWait


class BaseElement(object):
    def __init__(self, driver):
        self.__driver = driver
        self.__element = None
        # it = iter(locator)
        # for i in range(len(locator)):
        #     self.__element = WebDriverWait(driver=self.driver, timeout=3).until(
        #         lambda d: d.find_element(*locator[next(it)]))

    @property
    def element(self):
        return self.__element

    @element.setter
    def element(self, locator):
        self.__element = WebDriverWait(driver=self.__driver, timeout=3).until(
            lambda d: d.find_element(*locator))


class BasePage(object):
    def __init__(self, driver):
        self._driver = driver
        self._target = BaseElement(driver)

    def _is_loaded(self):
        assert self._url in self._driver.current_url

    def _load(self):
        self._driver.get(self._url)

    def get(self):
        try:
            self._is_loaded()
        except AssertionError:
            self._load()
        self._is_loaded()
