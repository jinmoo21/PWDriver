import configparser
import glob
import os
import re
from subprocess import Popen, PIPE

import requests
import tarfile
import zipfile

from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selenium.webdriver.safari.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from pwdriver.val import CONFIG_NAME, CHROME, CHROMEDRIVER, CHROMEDRIVER_API, CHROMEDRIVER_NAME, DRIVER, \
    EDGE, EDGEDRIVER, EDGEDRIVER_API, EDGEDRIVER_NAME, GECKO, GECKODRIVER, GECKODRIVER_API, GECKODRIVER_NAME, \
    OS_BIT, OS_NAME, ROOT_DIR, SAFARI, TAR_GZ, ZIP, ANDROID, IOS
from pwdriver import util

logger = util.get_logger('core')
driver_path = os.path.join(ROOT_DIR, DRIVER)
dir_regex = r'\S+[dD]river'


def __get_local_chrome_version() -> str:
    if OS_NAME == 'win':
        path = ['Program Files', 'Program Files (x86)']
        for loc in path:
            with Popen(fr'wmic datafile where name="C:\\{loc}\\Google\\Chrome\\Application\\chrome.exe" get '
                       r'version /value', stdout=PIPE, stderr=PIPE, shell=True) as p:
                output, error = p.communicate()
                if not error:
                    version = output.decode('ansi').strip().strip('Version=')
                    break
                else:
                    version = None
    elif OS_NAME == 'mac':
        with Popen(r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version', stdout=PIPE,
                   stderr=PIPE, shell=True) as p:
            output, error = p.communicate()
            version = output.decode('utf-8').strip().strip('Google Chrome ') if not error else None
    else:
        with Popen(r'google-chrome --version', stdout=PIPE, stderr=PIPE, shell=True) as p:
            output, error = p.communicate()
            version = output.decode('utf-8').strip().strip('Google Chrome ') if not error else None
    logger.info(f'Installed {CHROME} Browser version: {version}')
    if version is None:
        raise NotImplementedError(f'{CHROME} browser not installed.')
    return version


def __get_latest_chrome_version(version: str) -> str:
    latest_release = requests.get(f'{CHROMEDRIVER_API}/LATEST_RELEASE_{re.split(r"[.]", version)[0]}')
    global driver_path
    if not driver_path.endswith(latest_release.text):
        driver_path = os.path.join(driver_path, CHROME, latest_release.text)
    logger.info(f'Latest {CHROMEDRIVER} version: {latest_release.text}')
    return latest_release.text


def __download_chromedriver(version: str) -> None:
    global driver_path
    if not os.path.isfile(os.path.join(driver_path, CHROMEDRIVER_NAME)):
        logger.info(f'Not found executable {CHROMEDRIVER}. {CHROMEDRIVER} will be downloaded in \'{driver_path}\'.')
        download_url = f'{CHROMEDRIVER_API}/{version}/chromedriver_{OS_NAME}' + \
                       (OS_BIT if OS_NAME != 'win' else '32') + ZIP
        file = requests.get(download_url, stream=True)
        file_name = f'{CHROMEDRIVER}{ZIP}'
        with open(file_name, 'wb') as fd:
            logger.info(f'Downloading from {download_url}')
            for chunk in file:
                fd.write(chunk)
        zipfile.ZipFile(file_name).extractall(driver_path)
        os.remove(file_name)
        if not os.path.isfile(os.path.join(driver_path, CHROMEDRIVER_NAME)):
            os.rename(os.path.join(driver_path, util.get_pattern_matched_file(driver_path, dir_regex)[0]),
                      os.path.join(driver_path, CHROMEDRIVER_NAME))
    else:
        logger.info(f'Executable driver found: ({os.path.abspath(driver_path)})')


def setup_chromedriver() -> None:
    __download_chromedriver(__get_latest_chrome_version(__get_local_chrome_version()))
    global driver_path
    util.set_file_executable(os.path.join(driver_path, CHROMEDRIVER_NAME))
    os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(driver_path)}'
    driver_path = os.path.join(ROOT_DIR, DRIVER)


def __get_latest_gecko_version() -> str:
    version = re.split(r'/+', requests.get(f'{GECKODRIVER_API}/latest', allow_redirects=True).url)[-1]
    global driver_path
    if not driver_path.endswith(version):
        driver_path = os.path.join(driver_path, GECKO, version)
    return version


def __download_geckodriver(version: str) -> None:
    global driver_path
    if not os.path.isfile(os.path.join(driver_path, GECKODRIVER_NAME)):
        logger.info(f'Not found executable {GECKODRIVER}. {GECKODRIVER} will be downloaded in \'{driver_path}\'.')
        postfix = OS_NAME + (OS_BIT if OS_NAME != 'mac' else 'os') + (ZIP if OS_NAME == 'win' else TAR_GZ)
        download_url = f'{GECKODRIVER_API}/download/{version}/geckodriver-{version}-{postfix}'
        file = requests.get(download_url, stream=True)
        file_name = f'{GECKODRIVER}{ZIP}' if OS_NAME == 'win' else f'{GECKODRIVER}{TAR_GZ}'
        with open(file_name, 'wb') as fd:
            logger.info(f'Downloading from {download_url}')
            for chunk in file:
                fd.write(chunk)
        if OS_NAME == 'win':
            zipfile.ZipFile(file_name).extractall(driver_path)
        else:
            tar = tarfile.open(file_name, 'r:gz')
            tar.extractall(driver_path)
            tar.close()
        if not os.path.isfile(os.path.join(driver_path, GECKODRIVER_NAME)):
            os.rename(os.path.join(driver_path, util.get_pattern_matched_file(driver_path, dir_regex)[0]),
                      os.path.join(driver_path, GECKODRIVER_NAME))
        os.remove(file_name)
    else:
        logger.info(f'Executable driver found: ({os.path.abspath(driver_path)})')


def setup_geckodriver() -> None:
    __download_geckodriver(__get_latest_gecko_version())
    global driver_path
    util.set_file_executable(os.path.join(driver_path, GECKODRIVER_NAME))
    os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(driver_path)}'
    driver_path = os.path.join(ROOT_DIR, DRIVER)


def __get_local_edge_version() -> str:
    if OS_NAME == 'win':
        path = ['Program Files', 'Program Files (x86)']
        for loc in path:
            with Popen(fr'wmic datafile where name="C:\\{loc}\\Microsoft\\Edge\\Application\\msedge.exe" get '
                       r'version /value', stdout=PIPE, stderr=PIPE, shell=True) as p:
                output, error = p.communicate()
                if not error:
                    version = output.decode('ansi').strip().strip('Version=')
                    break
                else:
                    version = None
    elif OS_NAME == 'mac':
        with Popen(r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version', stdout=PIPE,
                   stderr=PIPE, shell=True) as p:
            output, error = p.communicate()
            version = output.decode('utf-8').strip().strip('Microsoft Edge ') if not error else None
    else:
        with Popen(r'microsoft-edge --version', stdout=PIPE, stderr=PIPE, shell=True) as p:
            output, error = p.communicate()
            version = output.decode('utf-8').strip().strip('Microsoft Edge ') if not error else None
    logger.info(f'Installed {EDGE} browser version: {version}')
    if version is None:
        raise NotImplementedError(f'{EDGE} browser not installed.')
    return version


def __download_edgedriver(version: str) -> None:
    global driver_path
    if not driver_path.endswith(version):
        driver_path = os.path.join(driver_path, EDGE, version)
    if not os.path.isfile(os.path.join(driver_path, EDGEDRIVER_NAME)):
        logger.info(f'Not found executable {EDGEDRIVER}. {EDGEDRIVER} will be downloaded in \'{driver_path}\'.')
        download_url = f'{EDGEDRIVER_API}/{version}/edgedriver_{OS_NAME}{OS_BIT}{ZIP}'
        file = requests.get(download_url, stream=True)
        file_name = f'{EDGEDRIVER}{ZIP}'
        with open(file_name, 'wb') as fd:
            logger.info(f'Downloading from {download_url}')
            for chunk in file:
                fd.write(chunk)
        zipfile.ZipFile(file_name).extractall(driver_path)
        if not os.path.isfile(os.path.join(driver_path, EDGEDRIVER_NAME)):
            os.rename(os.path.join(driver_path, util.get_pattern_matched_file(driver_path, dir_regex)[0]),
                      os.path.join(driver_path, EDGEDRIVER_NAME))
        os.remove(file_name)
    else:
        logger.info(f'Executable driver found: ({os.path.abspath(driver_path)})')


def setup_edgedriver() -> None:
    __download_edgedriver(__get_local_edge_version())
    global driver_path
    util.set_file_executable(os.path.join(driver_path, EDGEDRIVER_NAME))
    os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(driver_path)}'
    driver_path = os.path.join(ROOT_DIR, DRIVER)


class WebDriverFactory:
    _automation_target = None
    _mobile_caps = {}
    _automation_local = None
    _automation_url = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.optionxform = str
        config_path = glob.glob(os.path.join(ROOT_DIR, '**', CONFIG_NAME), recursive=True)
        if not config_path:
            raise NotImplementedError(f'Not found \'{CONFIG_NAME}\' configuration file in \'{ROOT_DIR}\'.')
        config.read(config_path[0])
        WebDriverFactory._automation_target = config.get('automation', 'target')
        if WebDriverFactory._automation_target not in [CHROME, GECKO, EDGE, SAFARI, ANDROID, IOS]:
            raise NotImplementedError(f'Unsupported browser name: {WebDriverFactory._automation_target}')
        if WebDriverFactory._automation_target in [ANDROID, IOS]:
            try:
                WebDriverFactory._mobile_caps = dict(config.items('mobile'))
            except configparser.NoSectionError:
                raise NotImplementedError(f'Capabilities for {WebDriverFactory._automation_target} must exist.')
        WebDriverFactory._automation_local = util.parse_boolean(config.get('automation', 'local'))
        if not WebDriverFactory._automation_local:
            WebDriverFactory._automation_url = config.get('automation', 'url')

    @classmethod
    def launch(cls, options=None) -> WebDriver:
        c = cls()
        from selenium import webdriver
        options_dict = {
            CHROME: webdriver.ChromeOptions(),
            GECKO: webdriver.FirefoxOptions(),
            EDGE: webdriver.EdgeOptions(),
            SAFARI: webdriver.safari.options.Options(),
            ANDROID: UiAutomator2Options().load_capabilities(c._mobile_caps),
            IOS: XCUITestOptions().load_capabilities(c._mobile_caps)
        }
        if c._automation_local:
            if c._automation_target == CHROME:
                setup_chromedriver()
                return webdriver.Chrome(options=options)
            if c._automation_target == GECKO:
                setup_geckodriver()
                return webdriver.Firefox(options=options)
            if c._automation_target == EDGE:
                setup_edgedriver()
                return webdriver.Edge(options=options)
            if c._automation_target == SAFARI:
                return webdriver.Safari(options=options if options is not None else options_dict[c._automation_target])
        if c._automation_target not in [ANDROID, IOS]:
            return webdriver.Remote(command_executor=c._automation_url,
                                    options=options if options is not None else options_dict[c._automation_target])
        from appium import webdriver
        return webdriver.Remote(command_executor=c._automation_url,
                                options=options_dict[c._automation_target])
