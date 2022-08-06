import os
import re

import requests
import tarfile
import zipfile

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException

from pwdriver.val import CONFIG_NAME, CHROME, CHROMEDRIVER, CHROMEDRIVER_API, CHROMEDRIVER_NAME, DRIVER, \
    EDGE, EDGEDRIVER, EDGEDRIVER_API, EDGEDRIVER_NAME, GECKO, GECKODRIVER, GECKODRIVER_API, GECKODRIVER_NAME, \
    OS_BIT, OS_NAME, ROOT_DIR, SAFARI, TAR_GZ, ZIP  # LOG, LOG_DIR,
from pwdriver import util

logger = util.get_logger('core')
driver_path = os.path.join(ROOT_DIR, DRIVER)


def _get_local_chrome_version():
    if OS_NAME == 'WIN':
        with os.popen(r'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get '
                      r'version /value') as stream:
            version = stream.read().strip().strip('Version=')
        if not version:
            with os.popen(r'wmic datafile where name="C:\\Program Files ('
                          r'x86)\\Google\\Chrome\\Application\\chrome.exe" get version /value') as stream:
                version = stream.read().strip().strip('Version=')
    elif OS_NAME == 'MAC':
        with os.popen(r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version') as stream:
            version = stream.read().strip('Google Chrome ').strip()
    else:
        with os.popen(r'google-chrome --version') as stream:
            version = stream.read().strip('Google Chrome ').strip()
    logger.info(f'Installed Chrome Browser version: {version}')
    return version


def _get_latest_chrome_version(version):
    latest_release = requests.get(f'{CHROMEDRIVER_API}/LATEST_RELEASE_{re.split(r"[.]", version)[0]}')
    global driver_path
    if not driver_path.endswith(latest_release.text):
        driver_path = os.path.join(driver_path, CHROME, latest_release.text)
    logger.info(f'Latest Chromedriver version: {latest_release.text}')
    return latest_release.text


def _download_chromedriver(version):
    global driver_path
    if not os.path.isfile(os.path.join(driver_path, CHROMEDRIVER_NAME)):
        logger.info('Not found executable chromedriver. Chromedriver will be downloaded.')
        download_url = f'{CHROMEDRIVER_API}/{version}/chromedriver_' \
                       + ('win32.zip' if OS_NAME == 'WIN' else 'mac64.zip' if OS_NAME == 'MAC' else 'linux64.zip')
        file = requests.get(download_url, stream=True)
        file_name = f'{CHROMEDRIVER}{ZIP}'
        with open(file_name, 'wb') as fd:
            logger.info(f'Downloading from {download_url}')
            for chunk in file:
                fd.write(chunk)
        zipfile.ZipFile(file_name).extractall(driver_path)
        os.remove(file_name)
        if not os.path.isfile(os.path.join(driver_path, CHROMEDRIVER_NAME)):
            os.rename(os.path.join(driver_path,
                                   util.get_pattern_matched_file(driver_path, r'\S+[dD]river')[0]),
                      os.path.join(driver_path, CHROMEDRIVER_NAME))
    else:
        logger.info(f'Executable driver found: ({os.path.abspath(driver_path)})')


def setup_chromedriver():
    _download_chromedriver(_get_latest_chrome_version(_get_local_chrome_version()))
    global driver_path
    util.set_file_executable(os.path.join(driver_path, CHROMEDRIVER_NAME))
    os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(driver_path)}'


def _get_latest_gecko_version():
    version = re.split(r'/+', requests.get(f'{GECKODRIVER_API}/latest', allow_redirects=True).url)[-1]
    global driver_path
    if not driver_path.endswith(version):
        driver_path = os.path.join(driver_path, GECKO, version)
    return version


def _download_geckodriver(version):
    global driver_path
    if not os.path.isfile(os.path.join(driver_path, GECKODRIVER_NAME)):
        logger.info(f'Not found executable geckodriver. Geckodriver will be downloaded.')
        download_url = f'{GECKODRIVER_API}/download/{version}/geckodriver-{version}-' \
                       + (('win64.zip' if OS_BIT == '64bit' else 'win32.zip') if OS_NAME == 'WIN'
                          else 'macos.tar.gz' if OS_NAME == 'MAC' else 'linux' + ('64.tar.gz' if OS_BIT == '64bit' else '32.tar.gz'))
        file = requests.get(download_url, stream=True)
        file_name = f'{GECKODRIVER}{ZIP}' if OS_NAME == 'WIN' else f'{GECKODRIVER}{TAR_GZ}'
        with open(file_name, 'wb') as fd:
            logger.info(f'Downloading from {download_url}')
            for chunk in file:
                fd.write(chunk)
        if OS_NAME == 'WIN':
            zipfile.ZipFile(file_name).extractall(driver_path)
        else:
            tar = tarfile.open(file_name, 'r:gz')
            tar.extractall(driver_path)
            tar.close()
        if not os.path.isfile(os.path.join(driver_path, GECKODRIVER_NAME)):
            os.rename(os.path.join(driver_path,
                                   util.get_pattern_matched_file(driver_path, r'\S+[dD]river')[0]),
                      os.path.join(driver_path, GECKODRIVER_NAME))
        os.remove(file_name)
    else:
        logger.info(f'Executable driver found: ({os.path.abspath(driver_path)})')


def setup_geckodriver():
    _download_geckodriver(_get_latest_gecko_version())
    global driver_path
    util.set_file_executable(os.path.join(driver_path, GECKODRIVER_NAME))
    os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(driver_path)}'


def _get_local_edge_version():
    if OS_NAME == 'WIN':
        with os.popen(r'wmic datafile where name="C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe" get '
                      r'version /value') as stream:
            version = stream.read().strip().strip('Version=')
        if not version:
            with os.popen(r'wmic datafile where name="C:\\Program Files ('
                          r'x86)\\Microsoft\\Edge\\Application\\msedge.exe" get version /value') as stream:
                version = stream.read().strip().strip('Version=')
    elif OS_NAME == 'MAC':
        with os.popen(r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version') as stream:
            version = stream.read().strip('Microsoft Edge ').strip()
    else:
        with os.popen(r'microsoft-edge --version') as stream:
            version = stream.read().strip('Microsoft Edge ').strip()
    logger.info(f'Installed Edge Browser version: {version}')
    return version


def _download_edgedriver(version):
    global driver_path
    if not driver_path.endswith(version):
        driver_path = os.path.join(driver_path, EDGE, version)
    if not os.path.isfile(os.path.join(driver_path, EDGEDRIVER_NAME)):
        logger.info(f'Not found executable edgedriver. Edgedriver will be downloaded.')
        download_url = f'{EDGEDRIVER_API}/{version}/edgedriver_' \
                       + (('win64.zip' if OS_BIT == '64bit' else 'win32.zip')
                          if OS_NAME == 'WIN' else 'mac64.zip' if OS_NAME == 'MAC' else 'linux64.zip')
        file = requests.get(download_url, stream=True)
        file_name = f'{EDGEDRIVER}{ZIP}'
        with open(file_name, 'wb') as fd:
            logger.info(f'Downloading from {download_url}')
            for chunk in file:
                fd.write(chunk)
        zipfile.ZipFile(file_name).extractall(driver_path)
        if not os.path.isfile(os.path.join(driver_path, EDGEDRIVER_NAME)):
            os.rename(os.path.join(driver_path,
                                   util.get_pattern_matched_file(driver_path, r'\S+[dD]river')[0]),
                      os.path.join(driver_path, EDGEDRIVER_NAME))
        os.remove(file_name)
    else:
        logger.info(f'Executable driver found: ({os.path.abspath(driver_path)})')


def setup_edgedriver():
    _download_edgedriver(_get_local_edge_version())
    global driver_path
    util.set_file_executable(os.path.join(driver_path, EDGEDRIVER_NAME))
    os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(driver_path)}'


class WebDriverFactory:
    def __init__(self):
        import configparser as cp
        config = cp.ConfigParser()
        import glob
        config_path = glob.glob(os.path.join(ROOT_DIR, '**', CONFIG_NAME), recursive=True)
        if not config_path:
            raise NotImplementedError(f'Not found \'{CONFIG_NAME}\' configuration file in directory.')
        config.read(config_path[0])
        self._automation_browser = config.get('automation', 'automation.browser')
        if self._automation_browser not in [CHROME, GECKO, EDGE, SAFARI]:
            raise NotImplementedError(f'Unsupported browser name: {self._automation_browser}')
        self._automation_local = util.parse_boolean(config.get('automation', 'automation.local'))
        if self._automation_browser in [EDGE, SAFARI] and not self._automation_local:
            raise NotImplementedError(f'{self._automation_browser} browser not installed on remote.')
        if not self._automation_local:
            self._automation_url = config.get('automation', 'automation.url')

    def launch(self, options=None):
        try:
            if self._automation_browser == CHROME and self._automation_local:
                setup_chromedriver()
                return webdriver.Chrome(options=options if options is not None else webdriver.ChromeOptions())
            if self._automation_browser == GECKO and self._automation_local:
                setup_geckodriver()
                return webdriver.Firefox(options=options if options is not None else webdriver.FirefoxOptions())
                # , service_log_path=os.path.join(ROOT_DIR, LOG_DIR, f'{GECKODRIVER}{LOG}'))
            if self._automation_browser == EDGE:
                setup_edgedriver()
                return webdriver.Edge(options=options if options is not None else webdriver.EdgeOptions())
            if self._automation_browser == SAFARI:
                if OS_NAME != 'MAC':
                    raise NotImplementedError('Cannot launch safari browser on Windows or Linux.')
                return webdriver.Safari()
            remote_options = webdriver.ChromeOptions() if self._automation_browser == CHROME \
                else webdriver.FirefoxOptions()
            return webdriver.Remote(command_executor=self._automation_url,
                                    options=options if options is not None else remote_options)
        except SessionNotCreatedException as e:
            if e.msg.find('unable to find binary in default location'):
                raise NotImplementedError(f'Browser not installed: {self._automation_browser}')
            logger.error(e.msg)
