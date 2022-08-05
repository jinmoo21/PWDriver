import platform
import sys

OS_NAME = 'WIN' if platform.system() == 'Windows' else 'MAC' if platform.system() == 'Darwin' else 'LINUX'
OS_BIT = platform.architecture()[0]
EXE = '.exe'
INI = '.ini'
LOG = '.log'
ZIP = '.zip'
TAR_GZ = '.tar.gz'
ROOT_DIR = sys.path[1]
CONFIG_NAME = f'config{INI}'
LOG_DIR = 'logs'
LOG_NAME = f'output{LOG}'
CHROMEDRIVER_API = 'https://chromedriver.storage.googleapis.com'
DRIVER = 'driver'
CHROME = 'chrome'
CHROMEDRIVER = f'{CHROME}{DRIVER}'
CHROMEDRIVER_NAME = f'{CHROMEDRIVER}{EXE}' if OS_NAME == 'WIN' else CHROMEDRIVER
GECKODRIVER_API = 'https://github.com/mozilla/geckodriver/releases'
GECKO = 'gecko'
GECKODRIVER = f'{GECKO}{DRIVER}'
GECKODRIVER_NAME = f'{GECKODRIVER}{EXE}' if OS_NAME == 'WIN' else GECKODRIVER
EDGEDRIVER_API = 'https://msedgedriver.azureedge.net'
EDGE = 'edge'
EDGEDRIVER = f'msedge{DRIVER}'
EDGEDRIVER_NAME = f'{EDGEDRIVER}{EXE}' if OS_NAME == 'WIN' else EDGEDRIVER
SAFARI = 'safari'
