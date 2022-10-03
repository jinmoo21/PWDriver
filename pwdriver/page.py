from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from pwdriver.util import get_logger

logger = get_logger('page')


class BaseElement(object):
    def __init__(self, driver):
        self.__driver = driver
        self.__timeout = 5
        self.__element = None

    @property
    def element(self) -> WebElement:
        return self.__element

    @element.setter
    def element(self, locator) -> None:
        self.__element = WebDriverWait(driver=self.__driver, timeout=self.__timeout).until(
            lambda d: d.find_element(*locator))

    @property
    def timeout(self) -> int:
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout: int) -> None:
        self.__timeout = timeout


class BasePage(object):
    def __init__(self, driver, timeout: int = None, jquery_defined: bool = None, angular_defined: bool = None):
        self._driver = driver
        self.__target = BaseElement(driver)
        self._url = None
        self._locator = None
        self.__timeout = 5 if timeout is None else timeout
        self.__jquery = False if jquery_defined is None else jquery_defined
        self.__angular = False if angular_defined is None else angular_defined

    @property
    def timeout(self) -> int:
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout: int) -> None:
        self.__target.timeout = timeout
        self.__timeout = timeout

    @property
    def jquery(self) -> bool:
        return self.__jquery

    @jquery.setter
    def jquery(self, jquery: bool) -> None:
        self.__jquery = jquery

    @property
    def angular(self) -> bool:
        return self.__angular

    @angular.setter
    def angular(self, angular: bool) -> None:
        self.__angular = angular

    def _is_loaded(self) -> None:
        assert self._url in self._driver.current_url

    def _load(self) -> None:
        self._driver.get(self._url)

    def get(self) -> None:
        try:
            self._is_loaded()
        except AssertionError:
            self._load()
        self._is_loaded()

    def _by(self, key: str) -> WebElement:
        self.__target.element = self._locator[key]
        return self.__target.element

    def wait_until_fully_loaded(self) -> None:
        if self.__jquery:
            try:
                WebDriverWait(driver=self._driver, timeout=self.__timeout).until(
                    lambda d: d.execute_script('return window.jQuery !== undefined'))
                WebDriverWait(driver=self._driver, timeout=self.__timeout).until(
                    lambda d: d.execute_script('return jQuery.active === 0'))
            except TimeoutException:
                self.__jquery = False
                logger.warning(f'{self._driver.current_url}: jquery is not defined.')
            # except JavascriptException:
            # self._jquery_defined = False
            # logger.warning(f'{self._driver.current_url}: jquery is not defined.')
        if self.__angular:
            try:
                WebDriverWait(driver=self._driver, timeout=self.__timeout).until(
                    lambda d: d.execute_script('return window.angular !== undefined'))
                WebDriverWait(driver=self._driver, timeout=self.__timeout).until(
                    lambda d: d.execute_script('return angular.element(document).injector() !== undefined'))
                WebDriverWait(driver=self._driver, timeout=self.__timeout).until(
                    lambda d: d.execute_script(
                        'return angular.element(document).injector().get(\'$http\').pendingRequests.length === 0'))
            except TimeoutException:
                self.__angular = False
                logger.warning(f'{self._driver.current_url}: angular is not defined.')
        WebDriverWait(driver=self._driver, timeout=self.__timeout).until(
            lambda d: d.execute_script('return document.readyState === \'complete\''))
        WebDriverWait(driver=self._driver, timeout=self.__timeout).until(
            lambda d: d.execute_script('return performance.timing.loadEventEnd !== 0'))
