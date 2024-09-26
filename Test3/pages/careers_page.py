from selenium.webdriver.common.by import By
from Test3.pages.base_page import BasePage


class CareersPage(BasePage):
    TEAMS_BLOCK = (By.CSS_SELECTOR, "h3.category-title-media")
    LOCATIONS_BLOCK = (By.CSS_SELECTOR, "h3.category-title-media.ml-0")
    LIFE_AT_INSIDER_BLOCK = (By.CSS_SELECTOR, "h2.elementor-heading-title.elementor-size-default")

    def are_career_blocks_visible(self):
        return (
                self.wait_for_element(self.LOCATIONS_BLOCK) and
                self.wait_for_element(self.TEAMS_BLOCK) and
                self.wait_for_element(self.LIFE_AT_INSIDER_BLOCK)
        )

    def navigate_to_qa_jobs(self):
        self.open_url("https://useinsider.com/careers/quality-assurance/")