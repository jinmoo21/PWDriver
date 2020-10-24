import os
import re
import requests
import tarfile
import zipfile

from selenium import webdriver

from val import CONFIG_NAME, CHROME, CHROMEDRIVER, CHROMEDRIVER_API, CHROMEDRIVER_NAME, DRIVER, EDGE, EDGEDRIVER, \
    EDGEDRIVER_API, EDGEDRIVER_NAME, GECKO, GECKODRIVER, GECKODRIVER_API, GECKODRIVER_NAME, IE, IEDRIVER, \
    IEDRIVER_API, IEDRIVER_NAME, LOG, LOG_DIR, MAC, OS_BIT, OS_NAME, ROOT_DIR, SAFARI, TAR_GZ, WIN, X64, ZIP
import util


logger = util.get_logger('core')


class WebDriverFactory:
    def _set_config(self):
        import configparser as cp
        config = cp.ConfigParser()
        config.read(os.path.join(ROOT_DIR, CONFIG_NAME))
        self._automation_browser = config.get('automation', 'automation.browser')
        if self._automation_browser not in [CHROME, GECKO, EDGE, IE, SAFARI]:
            raise NotImplementedError(f'Unsupported browser name: {self._automation_browser}')
        self._automation_local = util.parse_boolean(config.get('automation', 'automation.local'))
        if self._automation_browser in [EDGE, IE, SAFARI] and not self._automation_local:
            raise NotImplementedError(f'{self._automation_browser} browser not installed on remote.')
        if not self._automation_local:
            self._automation_url = config.get('automation', 'automation.url')

    def _get_local_chrome_version(self):
        if OS_NAME == WIN:
            with os.popen(r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version') as stream:
                version = re.split(r'\s+', stream.readlines()[2].strip())[2]
        else:
            with os.popen(r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version') as stream:
                version = stream.read().strip('Google Chrome ').strip()
        logger.info(f'Installed Chrome Browser version: {version}')
        return version

    def _get_latest_chrome_version(self, version):
        latest_release = requests.get(f'{CHROMEDRIVER_API}/LATEST_RELEASE_{re.split(r"[.]", version)[0]}')
        self._driver_path = os.path.join(ROOT_DIR, DRIVER, CHROME, latest_release.text)
        logger.info(f'Latest Chromedriver version: {latest_release.text}')
        return latest_release.text

    def _download_chromedriver(self, version):
        if not os.path.isfile(os.path.join(self._driver_path, CHROMEDRIVER_NAME)):
            logger.info('Not found executable chromedriver. Chromedriver will be downloaded.')
            self._download_url = f'{CHROMEDRIVER_API}/{version}/chromedriver_'\
                                 + ('win32.zip' if OS_NAME == WIN else 'mac64.zip')
            file = requests.get(self._download_url, stream=True)
            file_name = f'{CHROMEDRIVER}{ZIP}'
            with open(file_name, 'wb') as fd:
                logger.info(f'Downloading from {self._download_url}')
                for chunk in file:
                    fd.write(chunk)
            zipfile.ZipFile(file_name).extractall(self._driver_path)
            os.remove(file_name)
            if not os.path.isfile(os.path.join(self._driver_path, CHROMEDRIVER_NAME)):
                os.rename(os.path.join(self._driver_path,
                                       util.get_pattern_matched_file(self._driver_path, r'\S+[dD]river')[0]),
                          os.path.join(self._driver_path, CHROMEDRIVER_NAME))
        else:
            logger.info(f'Executable driver found: ({os.path.abspath(self._driver_path)})')

    def setup_chromedriver(self):
        self._download_chromedriver(self._get_latest_chrome_version(self._get_local_chrome_version()))
        util.set_file_executable(os.path.join(self._driver_path, CHROMEDRIVER_NAME))
        os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(self._driver_path)}'

    def _get_latest_gecko_version(self):
        version = re.split(r'/+', requests.get(f'{GECKODRIVER_API}/latest', allow_redirects=True).url)[-1]
        self._driver_path = os.path.join(ROOT_DIR, DRIVER, GECKO, version)
        return version

    def _download_geckodriver(self, version):
        if not os.path.isfile(os.path.join(self._driver_path, GECKODRIVER_NAME)):
            logger.info(f'Not found executable geckodriver. Geckodriver will be downloaded.')
            self._download_url = f'{GECKODRIVER_API}/download/{version}/geckodriver-{version}-'\
                                 + (('win64.zip' if OS_BIT == X64 else 'win32.zip') if OS_NAME == WIN
                                    else 'macos.tar.gz')
            file = requests.get(self._download_url, stream=True)
            file_name = f'{GECKODRIVER}{ZIP}' if OS_NAME == WIN else f'{GECKODRIVER}{TAR_GZ}'
            with open(file_name, 'wb') as fd:
                logger.info(f'Downloading from {self._download_url}')
                for chunk in file:
                    fd.write(chunk)
            if OS_NAME == WIN:
                zipfile.ZipFile(file_name).extractall(self._driver_path)
            else:
                tar = tarfile.open(file_name, 'r:gz')
                tar.extractall(self._driver_path)
                tar.close()
            if not os.path.isfile(os.path.join(self._driver_path, GECKODRIVER_NAME)):
                os.rename(os.path.join(self._driver_path,
                                       util.get_pattern_matched_file(self._driver_path, r'\S+[dD]river')[0]),
                          os.path.join(self._driver_path, GECKODRIVER_NAME))
            os.remove(file_name)
        else:
            logger.info(f'Executable driver found: ({os.path.abspath(self._driver_path)})')

    def setup_geckodriver(self):
        self._download_geckodriver(self._get_latest_gecko_version())
        util.set_file_executable(os.path.join(self._driver_path, GECKODRIVER_NAME))
        os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(self._driver_path)}'

    def _get_local_edge_version(self):
        if OS_NAME == WIN:
            with os.popen(r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version') as stream:
                version = re.split(r'\s+', stream.readlines()[2].strip())[2]
        else:
            with os.popen(r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version') as stream:
                version = stream.read().strip('Microsoft Edge ').strip()
        logger.info(f'Installed Edge Browser version: {version}')
        return version

    def _download_edgedriver(self, version):
        self._driver_path = os.path.join(ROOT_DIR, DRIVER, EDGE, version)
        if not os.path.isfile(os.path.join(self._driver_path, EDGEDRIVER_NAME)):
            logger.info(f'Not found executable edgedriver. Edgedriver will be downloaded.')
            self._download_url = f'{EDGEDRIVER_API}/{version}/edgedriver_'\
                                 + (('win64.zip' if OS_BIT == X64 else 'win32.zip') if OS_NAME == WIN
                                    else 'mac64.zip')
            file = requests.get(self._download_url, stream=True)
            file_name = f'{EDGEDRIVER}{ZIP}'
            with open(file_name, 'wb') as fd:
                logger.info(f'Downloading from {self._download_url}')
                for chunk in file:
                    fd.write(chunk)
            zipfile.ZipFile(file_name).extractall(self._driver_path)
            if not os.path.isfile(os.path.join(self._driver_path, EDGEDRIVER_NAME)):
                os.rename(os.path.join(self._driver_path,
                                       util.get_pattern_matched_file(self._driver_path, r'\S+[dD]river')[0]),
                          os.path.join(self._driver_path, EDGEDRIVER_NAME))
            os.remove(file_name)
        else:
            logger.info(f'Executable driver found: ({os.path.abspath(self._driver_path)})')

    def setup_edgedriver(self):
        self._download_edgedriver(self._get_local_edge_version())
        util.set_file_executable(os.path.join(self._driver_path, EDGEDRIVER_NAME))
        os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(self._driver_path)}'

    def _download_iedriver(self):
        self._driver_path = os.path.join(ROOT_DIR, DRIVER, IE)
        if not os.path.isfile(os.path.join(self._driver_path, IEDRIVER_NAME)):
            logger.info(f'Not found executable iedriver. IE driver will be downloaded.')
            self._download_url = f'{IEDRIVER_API}/3.150/IEDriverServer_Win32_3.150.1.zip'
            file = requests.get(self._download_url, stream=True)
            file_name = f'{IEDRIVER}{ZIP}'
            with open(file_name, 'wb') as fd:
                logger.info(f'Downloading from {self._download_url}')
                for chunk in file:
                    fd.write(chunk)
            zipfile.ZipFile(file_name).extractall(self._driver_path)
            if not os.path.isfile(os.path.join(self._driver_path, IEDRIVER_NAME)):
                os.rename(os.path.join(self._driver_path,
                                       util.get_pattern_matched_file(self._driver_path, r'\S+[dD]river')[0]),
                          os.path.join(self._driver_path, IEDRIVER_NAME))
            os.remove(file_name)
        else:
            logger.info(f'Executable driver found: ({os.path.abspath(self._driver_path)})')

    def setup_iedriver(self):
        self._download_iedriver()
        os.environ['PATH'] += f'{os.pathsep}{os.path.abspath(self._driver_path)}'

    def launch(self):
        self._set_config()
        from selenium.webdriver import DesiredCapabilities
        if self._automation_browser == CHROME and self._automation_local:
            self.setup_chromedriver()
            return webdriver.Chrome(desired_capabilities=DesiredCapabilities.CHROME.copy())
        elif self._automation_browser == GECKO and self._automation_local:
            self.setup_geckodriver()
            return webdriver.Firefox(desired_capabilities=DesiredCapabilities.FIREFOX.copy(),
                                     service_log_path=os.path.join(ROOT_DIR, LOG_DIR, f'{GECKODRIVER}{LOG}'))
        elif self._automation_browser == EDGE:
            self.setup_edgedriver()
            from msedge.selenium_tools import Edge, EdgeOptions
            options = EdgeOptions()
            options.use_chromium = True
            options.set_capability('platform', 'MAC' if OS_NAME == MAC else 'WINDOWS')
            return Edge(options=options)
        elif self._automation_browser == IE:
            if OS_NAME == MAC:
                raise NotImplementedError('Cannot launch IE browser on Mac.')
            self.setup_iedriver()
            from selenium.webdriver import IeOptions
            options = IeOptions()
            options.ignore_protected_mode_settings = True
            options.ensure_clean_session = True
            options.require_window_focus = True
            options.ignore_zoom_level = True
            return webdriver.Ie(desired_capabilities=DesiredCapabilities.INTERNETEXPLORER.copy(),
                                options=options)
        elif self._automation_browser == SAFARI:
            if OS_NAME == WIN:
                raise NotImplementedError('Cannot launch safari browser on Windows.')
            return webdriver.Safari(desired_capabilities=DesiredCapabilities.SAFARI.copy())
        return webdriver.Remote(command_executor=self._automation_url,
                                desired_capabilities=DesiredCapabilities.CHROME.copy()
                                if self._automation_browser == CHROME
                                else DesiredCapabilities.FIREFOX.copy())
