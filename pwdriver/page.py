from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class BaseElement(object):
    def __init__(self, driver):
        self.__driver = driver
        self.__element = None

    @property
    def element(self) -> WebElement:
        return self.__element

    @element.setter
    def element(self, locator) -> None:
        self.__element = WebDriverWait(driver=self.__driver, timeout=3).until(
            lambda d: d.find_element(*locator))


class BasePage(object):
    def __init__(self, driver):
        self._driver = driver
        self._target = BaseElement(driver)

    def _is_loaded(self) -> None:
        assert self._url in self._driver.current_url
        # it = iter(self._locator)
        # for i in range(len(self._locator)):
        #     self._target.element = self._locator[next(it)]

    def _load(self) -> None:
        self._driver.get(self._url)

    def get(self) -> None:
        try:
            self._is_loaded()
        except AssertionError:
            self._load()
        self._is_loaded()

    def _by(self, key) -> WebElement:
        self._target.element = self._locator[key]
        return self._target.element
