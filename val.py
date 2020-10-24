import os
import platform

OS_NAME = platform.system()
WIN = 'Windows'
MAC = 'Darwin'
OS_BIT = platform.architecture()
X86 = '32bit'
X64 = '64bit'
EXE = '.exe'
INI = '.ini'
LOG = '.log'
ZIP = '.zip'
TAR_GZ = '.tar.gz'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_NAME = f'config{INI}'
LOG_DIR = 'logs'
LOG_NAME = f'output{LOG}'
CHROMEDRIVER_API = 'https://chromedriver.storage.googleapis.com'
DRIVER = 'driver'
CHROME = 'chrome'
CHROMEDRIVER = f'{CHROME}{DRIVER}'
CHROMEDRIVER_NAME = f'{CHROMEDRIVER}{EXE}' if OS_NAME == WIN else CHROMEDRIVER
GECKODRIVER_API = 'https://github.com/mozilla/geckodriver/releases'
GECKO = 'gecko'
GECKODRIVER = f'{GECKO}{DRIVER}'
GECKODRIVER_NAME = f'{GECKODRIVER}{EXE}' if OS_NAME == WIN else GECKODRIVER
EDGEDRIVER_API = 'https://msedgedriver.azureedge.net'
EDGE = 'edge'
EDGEDRIVER = 'MicrosoftWebDriver'
EDGEDRIVER_NAME = f'{EDGEDRIVER}{EXE}' if OS_NAME == WIN else EDGEDRIVER
IEDRIVER_API = 'https://selenium-release.storage.googleapis.com'
IE = 'ie'
IEDRIVER = 'IEDriverServer'
IEDRIVER_NAME = f'{IEDRIVER}{EXE}'
SAFARI = 'safari'
