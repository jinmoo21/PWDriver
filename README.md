PWDriver (PyWebDriver)
======================
[![PyPI version](https://badge.fury.io/py/pwdriver.svg)](https://badge.fury.io/py/pwdriver)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Coverage](https://codecov.io/gh/jinmoo21/pwdriver/branch/master/graph/badge.svg)](https://codecov.io/gh/jinmoo21/pwdriver)
[![E2e test](https://github.com/jinmoo21/pwdriver/actions/workflows/python_test.yml/badge.svg)](https://github.com/jinmoo21/pwdriver/actions/workflows/python_test.yml)
[![Release status](https://github.com/jinmoo21/pwdriver/actions/workflows/python_release.yml/badge.svg)](https://github.com/jinmoo21/pwdriver/actions/workflows/python_release.yml)

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

config.ini 's contents be like this.

```ini
[automation]
;automation.browser: chrome, gecko, edge, safari
automation.browser=chrome
;automation.local: true, false
automation.local=true
automation.url=http://localhost:4444/wd/hub
```

### 3. Import WebDriverFactory.

Now, we could launch webdriver.   

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