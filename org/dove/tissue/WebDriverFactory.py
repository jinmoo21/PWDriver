import configparser as cp
import os
import platform
import re
import zipfile
import requests

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.ie.options import Options


class WebDriverFactory:
    def __init__(self):
        self.os_name = platform.system()
        self.os_bit = platform.architecture()
        self.config_file_name = "config.ini"
        self.download_url = 'Already installed.'
        self.chrome_driver_path = './driver/chrome'
        self.firefox_driver_path = './driver/firefox'
        self.edge_driver_path = './driver/edge'
        self.ie_driver_path = './driver/ie'

    def getConfig(self):
        config = cp.ConfigParser()
        config.read(f'./{self.config_file_name}')
        os.environ['browser'] = config.get('automation', 'test.automation.browser')
        os.environ['local'] = config.get('automation', 'test.automation.local')
        os.environ["url"] = config.get('automation', 'test.automation.url')

    def getChromeVersionFromShell(self):
        if self.os_name == 'Windows':
            with os.popen(r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version') as stream:
                version = re.split(r'\s+', stream.readlines()[2].strip())[2]
        elif self.os_name == 'Darwin':
            with os.popen(r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version') as stream:
                version = stream.read().strip('Google Chrome ').strip()
        return version

    def downloadChromeDriver(self, version):
        url = 'https://chromedriver.storage.googleapis.com'
        latest_release = requests.get(f'{url}/LATEST_RELEASE_{re.split(r"[.]", version)[0]}')
        self.chrome_driver_path += f'/{latest_release.text}'
        if not os.path.exists(self.chrome_driver_path):
            self.download_url = f'{url}/{latest_release.text}/chromedriver_'
            if self.os_name == 'Windows':
                self.download_url += 'win32.zip'
            elif self.os_name == 'Darwin':
                self.download_url += 'mac64.zip'
            elif self.os_name == 'Linux':
                self.download_url += 'linux64.zip'
            file = requests.get(self.download_url, stream=True)
            file_name = './chromedriver.zip'
            with open(file_name, 'wb') as fd:
                for chunk in file:
                    fd.write(chunk)
            zipfile.ZipFile(file_name).extractall(self.chrome_driver_path)
            os.remove(file_name)

    def chromeSetUp(self):
        self.downloadChromeDriver(self.getChromeVersionFromShell())

    #    def getFirefoxVersionFromShell(self):
    #        if os.environ["browser"] == 'firefox':
    #            if platform.system() == 'Windows':
    #                stream = os.popen('cd "C:\Program Files\Mozilla Firefox" & firefox -v|more')
    #                local_v = re.split(r'\s+', stream.read())[2]
    #            return local_v

    def downloadFirefoxDriver(self):
        url = 'https://github.com/mozilla/geckodriver/releases'
        latest_release = requests.get(f'{url}/latest', allow_redirects=True)
        gecko_version = re.split('[/]+', latest_release.url)[-1]
        self.firefox_driver_path += f'/{gecko_version}'
        if not os.path.exists(self.firefox_driver_path):
            if self.os_name == 'Windows':
                machine = 'win32.zip' if self.os_bit == '32bit' else 'win64.zip'
            elif self.os_name == 'Darwin':
                machine = 'macos.tar.gz'
            self.download_url = f'{url}/download/{gecko_version}/geckodriver-{gecko_version}-{machine}'
            file = requests.get(self.download_url, stream=True)
            file_name = f'./{machine}'
            with open(file_name, 'wb') as fd:
                for chunk in file:
                    fd.write(chunk)
            zipfile.ZipFile(file_name).extractall(self.firefox_driver_path)
            os.remove(file_name)

    def firefoxSetUp(self):
        self.downloadFirefoxDriver()

    def getEdgeVersionFromShell(self):
        if self.os_name == 'Windows':
            with os.popen(r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version') as stream:
                version = re.split(r'\s+', stream.readlines()[2].strip())[2]
        return version

    def downloadEdgeDriver(self, version):
        url = 'https://msedgedriver.azureedge.net'
        self.edge_driver_path += f'/{version}'
        if not os.path.exists(self.edge_driver_path):
            self.download_url = f'{url}/{version}/edgedriver_'
            if self.os_name == 'Windows':
                self.download_url += 'win64.zip' if self.os_bit == '64bit' else 'win32.zip'
            elif platform.system() == 'Darwin':
                self.download_url += 'mac64.zip'
            file = requests.get(self.download_url, stream=True)
            file_name = './msedgedriver.zip'
            with open(file_name, 'wb') as fd:
                for chunk in file:
                    fd.write(chunk)
            zipfile.ZipFile(file_name).extractall(self.edge_driver_path)
            os.remove(file_name)

    def edgeSetUp(self):
        self.downloadEdgeDriver(self.getEdgeVersionFromShell())

    def downloadInternetExplorerDriver(self):
        url = 'https://selenium-release.storage.googleapis.com'
        if not os.path.exists(self.ie_driver_path):
            self.download_url = f'{url}/3.150/IEDriverServer_Win32_3.150.1.zip'
            file = requests.get(self.download_url, stream=True)
            file_name = './IEDriverServer.zip'
            with open(file_name, 'wb') as fd:
                for chunk in file:
                    fd.write(chunk)
            zipfile.ZipFile(file_name).extractall(self.ie_driver_path)
            os.remove(file_name)

    def ieSetUp(self):
        self.downloadInternetExplorerDriver()

    def create(self):
        self.getConfig()
        if os.environ['browser'] == 'chrome':
            if os.environ["local"].lower() in ['true', 'y', 'yes']:
                self.chromeSetUp()
                return webdriver.Chrome(executable_path=f'{self.chrome_driver_path}/chromedriver.exe' if self.os_name == 'Windows'
                                        else f'{self.chrome_driver_path}/chromedriver')
        elif os.environ['browser'] == 'firefox':
            if os.environ["local"].lower() in ['true', 'y', 'yes']:
                self.firefoxSetUp()
                return webdriver.Firefox(executable_path=f'{self.firefox_driver_path}/geckodriver.exe' if platform.system() == 'Windows'
                                         else f'{self.firefox_driver_path}/geckodriver')
        elif os.environ['browser'] == 'MicrosoftEdge':
            self.edgeSetUp()
            return webdriver.Edge(executable_path=f'{self.edge_driver_path}/msedgedriver.exe' if platform.system() == 'Windows'
                                  else f'{self.edge_driver_path}/msedgedriver')
        elif os.environ['browser'] == 'internet explorer':
            self.ieSetUp()
            option = Options()
            option.ignore_protected_mode_settings = True
            option.ensure_clean_session = True
            option.require_window_focus = True
            option.ignore_zoom_level = True
            return webdriver.Ie(executable_path=f'{self.ie_driver_path}/IEDriverServer.exe', options=option)
        elif os.environ['browser'] == 'safari':
            return webdriver.Safari()
        return webdriver.Remote(desired_capabilities=DesiredCapabilities.CHROME.copy() if os.environ["browser"] == 'chrome'
                                else DesiredCapabilities.FIREFOX.copy(), command_executor=os.environ["url"])
