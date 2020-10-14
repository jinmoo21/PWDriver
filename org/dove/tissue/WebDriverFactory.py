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
    def getConfig(self):
        config_file_name = "config.ini"
        config = cp.ConfigParser()
        config.read("./" + config_file_name)
        os.environ["browser"] = config.get('automation', 'test.automation.browser')
        os.environ["local"] = config.get('automation', 'test.automation.local')
        os.environ["url"] = config.get('automation', 'test.automation.url')


    def getChromeVersionFromShell(self):
        if os.environ["browser"] == 'chrome':
            if platform.system() == 'Windows':
                stream = os.popen('reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version')
                local_v = re.split(r'\s+', stream.readlines()[2].strip())[2]
            return local_v

    def downloadChromeDriver(self, version):
        chrome_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + re.split(r'[.]', version)[0]
        print(chrome_url)
        resp_chrome = requests.get(chrome_url)
        print(resp_chrome.text)
        download_url = 'https://chromedriver.storage.googleapis.com/' + resp_chrome.text + '/chromedriver_'
        if platform.system() == 'Windows':
            download_url += 'win32.zip'
        elif platform.system() == 'Darwin':
            download_url += 'mac64.zip'
        elif platform.system() == 'Linux':
            download_url += 'linux64.zip'
        print(download_url)
        resp_download = requests.get(download_url, stream=True)
        chrome = './chromedriver.zip'
        with open(chrome, 'wb') as fd:
            for chunk in resp_download:
                fd.write(chunk)
        zipfile.ZipFile(chrome).extractall('./driver')
        os.remove(chrome)

    #    def chrome_version():
    #        osName = platform.system()
    #        if osName == 'Darwin':
    #            installPath = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'
    #        elif osName == 'Windows':
    #            installPath = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    #        elif osName == 'Linux':
    #            installPath = '/usr/bin/google-chrome'
    #        else:
    #            raise NotImplemented(f'Unknown OS: {osName}')
    #
    #        version = os.popen(f'{installPath} --version').read().strip('Google Chrome ').strip()
    #        return version

    def chromeSetUp(self):
        chrome_v = self.getChromeVersionFromShell()
        self.downloadChromeDriver(version=chrome_v)

    #    if os.path.isfile()

    def getFirefoxVersionFromShell(self):
        if os.environ["browser"] == 'firefox':
            if platform.system() == 'Windows':
                stream = os.popen('cd "C:\Program Files\Mozilla Firefox" & firefox -v|more')
                local_v = re.split(r'\s+', stream.read())[2]
            return local_v

    def downloadFirefoxDriver(self):
        firefox_url = 'https://github.com/mozilla/geckodriver/releases/latest'
        resp_firefox = requests.get(firefox_url, allow_redirects=True)
        temp = re.split(r'/', resp_firefox.url)
        download = ''
        gecko_v = temp[-1]
        print(gecko_v)
        if platform.system() == 'Windows':
            machine = 'win32.zip' if platform.architecture() == '32bit' else 'win64.zip'
        elif platform.system() == 'Darwin':
            machine = 'macos.tar.gz'
        elif platform.system() == 'Linux':
            machine = 'linux32.tar.gz' if platform.architecture() == '32bit' else 'linux64.tar.gz'
        for i in range(len(temp) - 2):
            download += temp[i] + '/'
        download_url = download + 'download/' + gecko_v + '/geckodriver-' + gecko_v + '-' + machine
        print(download_url)
        resp_download = requests.get(download_url, stream=True)
        firefox = './' + machine
        with open(firefox, 'wb') as fd:
            for chunk in resp_download:
                fd.write(chunk)
        zipfile.ZipFile(firefox).extractall('./driver')
        #    if os.path.exists(firefox):
        os.remove(firefox)

    def firefoxSetUp(self):
        self.downloadFirefoxDriver()

    def getEdgeVersionFromShell(self):
        if os.environ["browser"] == 'MicrosoftEdge':
            if platform.system() == 'Windows':
                stream = os.popen('reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version')
                local_v = re.split(r'\s+', stream.readlines()[2].strip())[2]
            return local_v

    def downloadEdgeDriver(self, version):
        download_url = 'https://msedgedriver.azureedge.net/' + version + '/edgedriver_'
        if platform.system() == 'Windows':
            download_url += 'win64.zip' if platform.architecture() == '64bit' else 'win32.zip'
        elif platform.system() == 'Darwin':
            download_url += 'mac64.zip'
        print(download_url)
        resp_download = requests.get(download_url, stream=True)
        edge = './edgedriver.zip'
        with open(edge, 'wb') as fd:
            for chunk in resp_download:
                fd.write(chunk)
        zipfile.ZipFile(edge).extractall('./driver')
        #    if os.path.exists(chrome):
        os.remove(edge)

    def edgeSetUp(self):
        edge_v = self.getEdgeVersionFromShell();
        self.downloadEdgeDriver(version=edge_v)

    def downloadInternetExplorerDriver(self):
        if platform.system() == 'Windows':
            download_url = 'https://selenium-release.storage.googleapis.com/3.150/IEDriverServer_Win32_3.150.1.zip'
            resp_download = requests.get(download_url, stream=True)
            ie = './iedriver.zip'
            with open(ie, 'wb') as fd:
                for chunk in resp_download:
                    fd.write(chunk)
            zipfile.ZipFile(ie).extractall('./driver')
            #    if os.path.exists(chrome):
            os.remove(ie)

    def ieSetUp(self):
        self.downloadInternetExplorerDriver()

    def setCapabilities(self):
        if os.environ["browser"] == 'chrome':
            capabilities = DesiredCapabilities.CHROME.copy()
        elif os.environ["browser"] == 'firefox':
            capabilities = DesiredCapabilities.FIREFOX.copy()
        return capabilities

    def create(self):
        self.getConfig()
        if os.environ['browser'] == 'chrome':
            if os.environ["local"].lower() in ['true', 'y', 'yes']:
                self.chromeSetUp()
                return webdriver.Chrome(
                    executable_path='./driver/chromedriver.exe' if platform.system() == 'Windows' else './driver/chromedriver')
        elif os.environ['browser'] == 'firefox':
            if os.environ["local"].lower() in ['true', 'y', 'yes']:
                self.firefoxSetUp()
                return webdriver.Firefox(
                    executable_path='./driver/geckodriver.exe' if platform.system() == 'Windows' else './driver/geckodriver')
        elif os.environ['browser'] == 'MicrosoftEdge':
            self.edgeSetUp()
            return webdriver.Edge(
                executable_path='./driver/msedgedriver.exe' if platform.system() == 'Windows' else './driver/msedgedriver')
        elif os.environ['browser'] == 'internet explorer':
            self.ieSetUp()
            option = Options()
            option.ignore_protected_mode_settings = True
            option.ensure_clean_session = True
            option.require_window_focus = True
            option.ignore_zoom_level = True
            return webdriver.Ie(executable_path='./driver/IEDriverServer.exe', options=option)
        elif os.environ['browser'] == 'safari':
            return webdriver.Safari()
        capabilities = self.setCapabilities()
        return webdriver.Remote(desired_capabilities=capabilities, command_executor=os.environ["url"])
