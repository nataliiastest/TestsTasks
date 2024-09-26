from selenium.webdriver.common.by import By
from Test3.pages.base_page import BasePage


class HomePage(BasePage):
    COMPANY_MENU = (By.LINK_TEXT, "Company")
    CAREERS_MENU = (By.LINK_TEXT, "Careers")

    def is_home_page_opened(self):
        return "Insider" in self.driver.title

    def navigate_to_careers(self):
        self.click(self.COMPANY_MENU)
        self.click(self.CAREERS_MENU)
