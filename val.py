import platform

OS_NAME = platform.system()
OS_BIT = platform.architecture()
EXE = '.exe'
INI = '.ini'
LOG = '.log'
ZIP = '.zip'
TAR_GZ = '.tar.gz'
CONFIG_NAME = f'config{INI}'
LOG_DIR = 'logs'
LOG_FILE = 'output'
CHROMEDRIVER_API = 'https://chromedriver.storage.googleapis.com'
DRIVER = 'driver'
CHROME = 'chrome'
CHROMEDRIVER = f'{CHROME}{DRIVER}'
CHROMEDRIVER_NAME = f'{CHROMEDRIVER}{EXE}' if OS_NAME == 'Windows' else CHROMEDRIVER
GECKODRIVER_API = 'https://github.com/mozilla/geckodriver/releases'
GECKO = 'gecko'
GECKODRIVER = f'{GECKO}{DRIVER}'
GECKODRIVER_NAME = f'{GECKODRIVER}{EXE}' if OS_NAME == 'Windows' else GECKODRIVER
EDGEDRIVER_API = 'https://msedgedriver.azureedge.net'
EDGE = 'edge'
EDGEDRIVER = f'{EDGE}{DRIVER}'
EDGEDRIVER_NAME = f'{EDGEDRIVER}{EXE}' if OS_NAME == 'Windows' else EDGEDRIVER
IEDRIVER_API = 'https://selenium-release.storage.googleapis.com'
IE = 'ie'
IEDRIVER = f'{IE}{DRIVER}'
IEDRIVER_NAME = f'{IEDRIVER}{EXE}'
SAFARI = 'safari'
