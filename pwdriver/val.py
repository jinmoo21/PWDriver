import platform
import sys

PLATFORM_DICT = {
    'Windows': 'win',
    'Darwin': 'mac',
    'Linux': 'linux'
}
OS_NAME = PLATFORM_DICT[platform.system()]
OS_BIT = '64' if platform.architecture()[0] == '64bit' else '32'
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
CHROMEDRIVER_NAME = f'{CHROMEDRIVER}{EXE}' if OS_NAME == 'win' else CHROMEDRIVER
GECKODRIVER_API = 'https://github.com/mozilla/geckodriver/releases'
GECKO = 'gecko'
GECKODRIVER = f'{GECKO}{DRIVER}'
GECKODRIVER_NAME = f'{GECKODRIVER}{EXE}' if OS_NAME == 'win' else GECKODRIVER
EDGEDRIVER_API = 'https://msedgedriver.azureedge.net'
EDGE = 'edge'
EDGEDRIVER = f'ms{EDGE}{DRIVER}'
EDGEDRIVER_NAME = f'{EDGEDRIVER}{EXE}' if OS_NAME == 'win' else EDGEDRIVER
SAFARI = 'safari'
ANDROID = 'android'
IOS = 'ios'
