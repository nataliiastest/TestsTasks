import os

from selenium.common import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, time


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def wait_for_element(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element

    def take_screenshot(self, test_name):
        """
        Takes a screenshot and saves it to a 'screenshots' directory with a timestamp.
        """
        screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
        # Create directory if it doesn't exist
        os.makedirs(screenshots_dir, exist_ok=True)

        # Create a unique filename with the test name and timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        screenshot_file = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")

        # Save the screenshot
        self.driver.save_screenshot(screenshot_file)
        print(f"Screenshot saved to {screenshot_file}")

    def click(self, locator):
        for _ in range(3):  # Retry 3 times
            try:
                element = self.wait_for_element(locator)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)  # Scroll into view
                element.click()  # Attempt to click
                return
            except ElementClickInterceptedException:
                time.sleep(0.5)  # Wait a bit before retrying
        raise Exception("Element could not be clicked after multiple attempts.")