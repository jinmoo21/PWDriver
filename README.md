PWDriver (PyWebDriver)
======================

## Motivation

To simplify automation settings of each different version, and browser.

##### Support:

- ChromeDriver

- GeckoDriver

- EdgeDriver (Chromium)

- IEDriver

##### Before:

- You have to check your local browser's version

- You have to download driver on each website

- You have to set path to this driver like this:

```python
from selenium import webdriver

webdriver.Chrome('YOUR_CHROMEDRIVER_PATH')
```

## Usage

### 1. Install:

```bash
pip install pwdriver
```

### 2. Make 'config.ini' file and locate in your project directory.

config.ini 's contents be like this.

```ini
[automation]
;automation.browser: chrome, gecko, edge, ie, safari
automation.browser=chrome
;automation.local: true, false
automation.local=true
automation.url=http://localhost:4444/wd/hub
```

### 3. Import WebDriverFactory.

Now, we could launch webdriver.

'automation.browser' you set will be created.   

```python
from pwdriver.core import WebDriverFactory

driver = WebDriverFactory().launch()
```

### Different Usage(using selenium)

Use with Chrome:

```python
from selenium import webdriver
from pwdriver.core import WebDriverFactory

WebDriverFactory().setup_chromedriver()
driver = webdriver.Chrome()
```

Use with FireFox:

```python
from selenium import webdriver
from pwdriver.core import WebDriverFactory

WebDriverFactory().setup_geckodriver()
driver = webdriver.Firefox()
```

Use with Edge:

```python

from selenium import webdriver
from pwdriver.core import WebDriverFactory

WebDriverFactory().setup_edgedriver()
driver = webdriver.Edge()
```


Use with IE:

```python
from selenium import webdriver
from pwdriver.core import WebDriverFactory

WebDriverFactory().setup_iedriver()
driver = webdriver.Ie()
```
