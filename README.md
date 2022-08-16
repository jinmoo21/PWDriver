# PWDriver (PyWebDriver)

[![E2e test](https://github.com/jinmoo21/pwdriver/actions/workflows/python_test.yml/badge.svg)](https://github.com/jinmoo21/pwdriver/actions/workflows/python_test.yml)
[![Code Coverage](https://codecov.io/gh/jinmoo21/pwdriver/branch/master/graph/badge.svg)](https://codecov.io/gh/jinmoo21/pwdriver)

[![Release status](https://github.com/jinmoo21/pwdriver/actions/workflows/python_release.yml/badge.svg)](https://github.com/jinmoo21/pwdriver/actions/workflows/python_release.yml)
[![PyPI version](https://badge.fury.io/py/pwdriver.svg)](https://badge.fury.io/py/pwdriver)

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/jinmoo21/PWDriver/blob/master/LICENSE)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fjinmoo21%2FPWDriver.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fjinmoo21%2FPWDriver?ref=badge_shield)

## Motivation

To simplify automation settings of each different version, and browser.

##### Support:

- ChromeDriver

- GeckoDriver

- EdgeDriver (Chromium)

- ~~IEDriver~~

## Usage

### 1. Install:

```bash
pip install pwdriver
```

### 2. Make 'config.ini' file and locate in your project directory.

config.ini 's contents look like this.

```ini
[automation]
;automation.browser: chrome, gecko, edge, safari
automation.browser=safari
;automation.local: true, false
automation.local=false
automation.url=http://192.168.0.19:4444
```

### 3. Import WebDriverFactory.

Now, we can launch webdriver.   

```python
from pwdriver.core import WebDriverFactory

driver = WebDriverFactory().launch()
```

### Different Usage(using selenium)

Use with Chrome:

```python
from selenium import webdriver
from pwdriver import core

core.setup_chromedriver()
driver = webdriver.Chrome()
```

Use with FireFox:

```python
from selenium import webdriver
from pwdriver import core

core.setup_geckodriver()
driver = webdriver.Firefox()
```

Use with Edge:

```python
from selenium import webdriver
from pwdriver import core

core.setup_edgedriver()
driver = webdriver.Edge()
```

## Page object models

Page object models pattern makes our test cases more concise and readable.

The good news is, we can use Page Objects with this.

There is an example that searching for keyword on `www.bing.com` and verifying url, title.

For using this, we are going to create modules that page object classes and test cases.

Modules that page elements and locators already implemented, so nevermind.


### Page Object Class

`pages/bing_page.py` look like this.

```python
from selenium.webdriver.common.by import By

from pwdriver.page import BasePage


class BingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self._url = 'https://www.bing.com'
        self._locator = {
            'input': (By.CSS_SELECTOR, 'input#sb_form_q'),
            'search': (By.CSS_SELECTOR, 'label#search_icon')
        }

    def type_keyword(self, text) -> None:
        self._by('input').send_keys(text)

    def click_search(self) -> BasePage:
        self._by('search').click()
        return BingPage(BasePage)
```

### Test case

`page_object.py` look like this.

```python
from pwdriver.core import WebDriverFactory
from tests.pages.bing_page import BingPage

import unittest


class BrowserTest(unittest.TestCase):
    def setUp(self):
        self.driver = WebDriverFactory().launch()

    def tearDown(self):
        self.driver.quit()

    def test_something(self):
        page = BingPage(self.driver)
        page.get()
        page.type_keyword("치킨")
        page.click_search()
        self.assertIn("https://www.bing.com/search?q=%EC%B9%98%ED%82%A8", self.driver.current_url)
        self.assertEqual("치킨 - Search", self.driver.title)


if __name__ == '__main__':
    unittest.main()
```

## Logging and Event listener

If we want to use logging or want to see what events occured in webdriver,

we can use get_logger or EventListener().

See below example code.

```python
from selenium.webdriver.support.events import EventFiringWebDriver

from pwdriver.core import WebDriverFactory
from pwdriver.listener import EventListener
from pwdriver.util import get_logger

logger = get_logger('eventdriver')

core = WebDriverFactory().launch()
driver = EventFiringWebDriver(core, EventListener())
logger.info('WebDriver created.')
```

* Log level: `debug`, `info`, `warning`, `error`, `critical`
* WebDriver event: `navigate`, `execute script`
* WebElement event: `find`, `click`, `change value` 

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fjinmoo21%2FPWDriver.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fjinmoo21%2FPWDriver?ref=badge_large)