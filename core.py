import os
import re
import requests
import tarfile
import zipfile

from selenium import webdriver

import util
import val

logger = util.get_logger('core')


class WebDriverFactory:
    def __init__(self):
        self._automation_browser = None
        self._automation_local = True
        self._automation_url = None

    def _set_config(self):
        import configparser as cp
        config = cp.ConfigParser()
        config.read(val.CONFIG_NAME)
        self._automation_browser = config.get('automation', 'automation.browser')
        if self._automation_browser == val.CHROME:
            self._driver_path = f'{val.DRIVER}{os.path.sep}{val.CHROME}'
        elif self._automation_browser == val.GECKO:
            self._driver_path = f'{val.DRIVER}{os.path.sep}{val.GECKO}'
        elif self._automation_browser == val.EDGE:
            self._driver_path = f'{val.DRIVER}{os.path.sep}{val.EDGE}'
        elif self._automation_browser == val.IE:
            self._driver_path = f'{val.DRIVER}{os.path.sep}{val.IE}'
        else:
            raise NotImplementedError(f'Unsupported browser name: {self._automation_browser}')
        self._automation_local = util.parse_boolean(config.get('automation', 'automation.local'))
        if self._automation_browser in [val.EDGE, val.IE, val.SAFARI] and not self._automation_local:
            raise NotImplementedError(f'{self._automation_browser} browser not installed on remote.')
        if not self._automation_local:
            self._automation_url = config.get('automation', 'automation.url')

    def _get_local_chrome_version(self):
        if val.OS_NAME == 'Windows':
            with os.popen(r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version') as stream:
                version = re.split(r'\s+', stream.readlines()[2].strip())[2]
        else:
            with os.popen(r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version') as stream:
                version = stream.read().strip('Google Chrome ').strip()
        logger.info(f'Installed Chrome Browser version: {version}')
        return version

    def _get_latest_chrome_version(self, version):
        latest_release = requests.get(f'{val.CHROMEDRIVER_API}/LATEST_RELEASE_{re.split(r"[.]", version)[0]}')
        try:
            self._driver_path += f'{os.path.sep}{latest_release.text}'
        except AttributeError:
            self._driver_path = f'{val.DRIVER}{os.path.sep}{val.CHROME}{os.path.sep}{latest_release.text}'
        logger.info(f'Latest Chromedriver version: {latest_release.text}')
        return latest_release.text

    def _download_chromedriver(self, version):
        if not os.path.exists(self._driver_path):
            logger.info('Not found executable chromedriver. Chromedriver will be downloaded.')
            self._download_url = f'{val.CHROMEDRIVER_API}/{version}/chromedriver_'
            if val.OS_NAME == 'Windows':
                self._download_url += 'win32.zip'
            else:
                self._download_url += 'mac64.zip'
            file = requests.get(self._download_url, stream=True)
            file_name = f'{val.CHROMEDRIVER}{val.ZIP}'
            with open(file_name, 'wb') as fd:
                logger.info(f'Downloading from {self._download_url}')
                for chunk in file:
                    fd.write(chunk)
            zipfile.ZipFile(file_name).extractall(self._driver_path)
            os.remove(file_name)
        else:
            logger.info(f'Executable driver found: ({os.path.abspath(self._driver_path)})')

    def setup_chromedriver(self):
        self._download_chromedriver(self._get_latest_chrome_version(self._get_local_chrome_version()))
        util.set_file_executable(f'{self._driver_path}'
                                 f'{os.path.sep}{val.CHROMEDRIVER_NAME}')
        os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(self._driver_path)}'

    def _get_latest_gecko_version(self):
        version = re.split(r'[/]+', requests.get(f'{val.GECKODRIVER_API}/latest', allow_redirects=True).url)[-1]
        try:
            self._driver_path += f'{os.path.sep}{version}'
        except AttributeError:
            self._driver_path = f'{val.DRIVER}{os.path.sep}{val.GECKO}{os.path.sep}{version}'
        return version

    def _download_geckodriver(self, version):
        if not os.path.exists(self._driver_path):
            logger.info(f'Not found executable geckodriver. Geckodriver will be downloaded.')
            self._download_url = f'{val.GECKODRIVER_API}/download/{version}' \
                                 f'/geckodriver-{version}-'
            if val.OS_NAME == 'Windows':
                self._download_url += 'win32.zip' if val.OS_BIT == '32bit' else 'win64.zip'
            else:
                self._download_url += 'macos.tar.gz'
            file = requests.get(self._download_url, stream=True)
            file_name = f'{val.GECKODRIVER}{val.ZIP}' if val.OS_NAME == 'Windows' else f'{val.GECKODRIVER}{val.TAR_GZ}'
            with open(file_name, 'wb') as fd:
                logger.info(f'Downloading from {self._download_url}' if self._download_url is not None
                            else 'Executable driver found.')
                for chunk in file:
                    fd.write(chunk)
            if val.OS_NAME == 'Windows':
                zipfile.ZipFile(file_name).extractall(self._driver_path)
            else:
                tar = tarfile.open(file_name, 'r:gz')
                tar.extractall(self._driver_path)
                tar.close()
            os.remove(file_name)
        else:
            logger.info(f'Executable driver found: ({self._driver_path})')

    def setup_geckodriver(self):
        self._download_geckodriver(self._get_latest_gecko_version())
        util.set_file_executable(f'{self._driver_path}'
                                 f'{os.path.sep}{val.GECKODRIVER_NAME}')
        os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(self._driver_path)}'

    def _get_local_edge_version(self):
        if val.OS_NAME == 'Windows':
            with os.popen(r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version') as stream:
                version = re.split(r'\s+', stream.readlines()[2].strip())[2]
        else:
            with os.popen(r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version') as stream:
                version = stream.read().strip('Microsoft Edge ').strip()
        logger.info(f'Installed Edge Browser version: {version}')
        return version

    def _download_edgedriver(self, version):
        try:
            self._driver_path += f'{os.path.sep}{version}'
        except AttributeError:
            self._driver_path = f'{val.DRIVER}{os.path.sep}{val.CHROME}{os.path.sep}{version}'
        if not os.path.exists(self._driver_path):
            logger.info(f'Not found executable edgedriver. Edgedriver will be downloaded.')
            self._download_url = f'{val.EDGEDRIVER_API}/{version}/edgedriver_'
            if val.OS_NAME == 'Windows':
                self._download_url += 'win64.zip' if val.OS_BIT == '64bit' else 'win32.zip'
            else:
                self._download_url += 'mac64.zip'
            file = requests.get(self._download_url, stream=True)
            file_name = f'{val.EDGEDRIVER}{val.ZIP}'
            with open(file_name, 'wb') as fd:
                logger.info(f'Downloading from {self._download_url}' if self._download_url is not None
                            else 'Executable driver found.')
                for chunk in file:
                    fd.write(chunk)
            zipfile.ZipFile(file_name).extractall(self._driver_path)
            os.remove(file_name)
        else:
            logger.info(f'{self._download_url}')

    def setup_edgedriver(self):
        self._download_edgedriver(self._get_local_edge_version())
        util.set_file_executable(f'{self._driver_path}'
                                 f'{os.path.sep}{val.EDGEDRIVER_NAME}')
        os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(self._driver_path)}'

    def _download_iedriver(self):
        if not os.path.exists(self._driver_path):
            logger.info(f'Not found executable iedriver. IE driver will be downloaded.')
            self._download_url = f'{val.IEDRIVER_API}/3.150/IEDriverServer_Win32_3.150.1.zip'
            file = requests.get(self._download_url, stream=True)
            file_name = f'{val.IEDRIVER}{val.ZIP}'
            with open(file_name, 'wb') as fd:
                logger.info(f'Downloading from {self._download_url}' if self._download_url is not None
                            else 'Executable driver found.')
                for chunk in file:
                    fd.write(chunk)
            zipfile.ZipFile(file_name).extractall(self._driver_path)
            os.remove(file_name)
        else:
            logger.info(f'{self._download_url}')

    def setup_iedriver(self):
        self._download_iedriver()
        os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(self._driver_path)}'

    def launch(self):
        self._set_config()
        if self._automation_browser == val.CHROME and self._automation_local:
            self.setup_chromedriver()
            return webdriver.Chrome()
        elif self._automation_browser == val.GECKO and self._automation_local:
            self.setup_geckodriver()
            return webdriver.Firefox()
        elif self._automation_browser == val.EDGE:
            self.setup_edgedriver()
            return webdriver.Edge()
        elif self._automation_browser == val.IE:
            self.setup_iedriver()
            from selenium.webdriver.ie.options import Options
            ie_options = Options()
            ie_options.ignore_protected_mode_settings = True
            ie_options.ensure_clean_session = True
            ie_options.require_window_focus = True
            ie_options.ignore_zoom_level = True
            return webdriver.Ie(options=ie_options)
        elif self._automation_browser == val.SAFARI:
            return webdriver.Safari()
        from selenium.webdriver import DesiredCapabilities
        return webdriver.Remote(command_executor=self._automation_url,
                                desired_capabilities=DesiredCapabilities.CHROME.copy()
                                if self._automation_browser == val.CHROME
                                else DesiredCapabilities.FIREFOX.copy())
