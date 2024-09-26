import logging
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Test3.pages.base_page import BasePage
import time

# Config logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QAJobsPage(BasePage):
    SEE_ALL_JOBS_BTN = (By.XPATH, "//a[text()='See all QA jobs']")
    FILTER_HELPER = (By.CSS_SELECTOR, "h3.mb-0")
    LOCATION_FILTER = (By.XPATH, "//span[@id='select2-filter-by-location-container']")
    DEPARTMENT_FILTER = (By.XPATH, "//span[@id='select2-filter-by-department-container']")
    JOB_TITLES = (By.XPATH, "//h3[contains(text(), 'Quality Assurance')]")
    JOB_LOCATIONS = (By.XPATH, "//p[contains(text(), 'Istanbul, Turkey')]")
    VIEW_ROLE_BUTTON = (By.XPATH, "//a[contains(text(),'View Role')]")
    COOKIE_CONSENT_BUTTON = (By.CSS_SELECTOR, "#wt-cli-accept-all-btn")

    def filter_jobs(self, location="Istanbul, Turkey", department="Quality Assurance"):
        self.accept_cookie_consent()  # Ensure cookies are handled

        # Click on the location filter dropdown
        self.click(self.LOCATION_FILTER)  # Open location filter
        self.select_filter_option(location)  # Select location

        # Click on the department filter dropdown
        self.click(self.DEPARTMENT_FILTER)  # Open department filter
        self.select_filter_option(department)  # Select department

    def select_filter_option(self, option_text):
        # Find the option and click it
        option_locator = (By.XPATH, f"//li[contains(text(), '{option_text}')]")
        option_element = self.wait_for_element(option_locator)
        self.click(option_locator)  # Use the locator tuple here

    def are_filtered_jobs_present(self):
        # Find job titles and locations
        job_titles = self.driver.find_elements(By.XPATH, "//p[contains(text(),'Quality Assurance Engineer')]")
        job_locations = self.driver.find_elements(By.XPATH, "//div[contains(text(),'Istanbul, Turkey')]")

        # Check if there are any jobs and if they match the expected criteria
        if not job_titles or not job_locations:
            logger.warning("No job titles or locations found.")
            return False

        for job_title, job_location in zip(job_titles, job_locations):
            if "Quality Assurance" not in job_title.text:
                logger.warning(f"Job title mismatch: {job_title.text}")
                return False
            if "Istanbul, Turkey" not in job_location.text:
                logger.warning(f"Job location mismatch: {job_location.text}")
                return False

        return True

    def click_view_role(self):
        # Use ActionChains to hover over the View Role button
        try:
            logger.info("Waiting for the View Role button to be present...")
            view_role_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.VIEW_ROLE_BUTTON)
            )

            logger.info("Hovering over the View Role button...")
            actions = ActionChains(self.driver)
            actions.move_to_element(view_role_button).perform()

            # Now wait for the button to be clickable after hover
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.VIEW_ROLE_BUTTON)
            )

            # Locate the button again to avoid stale element reference
            view_role_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.VIEW_ROLE_BUTTON)
            )

            logger.info("Clicking the View Role button...")
            view_role_button.click()

            # Wait for the new tab to open
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)

            # Switch to the new tab
            new_window = [window for window in self.driver.window_handles if window != self.driver.current_window_handle][0]
            self.driver.switch_to.window(new_window)

            # Optionally, wait for the new page to load
            WebDriverWait(self.driver, 10).until(lambda d: "jobs.lever.co" in d.current_url)
            logger.info("Successfully switched to the new tab.")
        except TimeoutException:
            logger.error("Timeout: View Role button not found or not clickable.", exc_info=True)
            raise  # Re-raise the exception to be caught in the test case

    def accept_cookie_consent(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            # Wait for the cookie consent button to be clickable
            cookie_consent_btn = wait.until(EC.element_to_be_clickable(self.COOKIE_CONSENT_BUTTON))
            # Click the cookie consent button to accept it
            cookie_consent_btn.click()
            logger.info("Cookie consent accepted.")
        except Exception as e:
            logger.error(f"Cookie consent button not found or could not be clicked: {e}", exc_info=True)

    def scroll_to_qa_btn(self):
        # Handle cookie consent first
        self.accept_cookie_consent()
        # Wait for the QA jobs button to be present and scroll it into view
        qa_btn = self.wait_for_element(self.SEE_ALL_JOBS_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", qa_btn)
        return qa_btn

    def scroll_to_element(self, element):
        """Scroll to the specified element."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Optional: add a brief pause to ensure the scroll is complete
        logger.debug("Scrolled to element.")

    def scroll_to_location_filter(self):
        """Scroll to the location filter element."""
        location_filter_element = self.wait_for_element(self.LOCATION_FILTER)
        self.scroll_to_element(location_filter_element)
