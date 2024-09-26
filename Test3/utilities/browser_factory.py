from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


class BrowserFactory:
    def __init__(self, browser_name):
        self.browser_name = browser_name

    def get_driver(self):
        if self.browser_name == "chrome":
            #Used ChromeDriverManager for Chrome
            chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
            return webdriver.Chrome(service=chrome_service)
        elif self.browser_name == "firefox":
            #Used GeckoDriverManager for Firefox
            firefox_service = FirefoxService(executable_path=GeckoDriverManager().install())
            return webdriver.Firefox(service=firefox_service)
        else:
            raise Exception(f"Unsupported browser: {self.browser_name}")
