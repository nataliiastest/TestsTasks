import unittest
from Test3.pages.home_page import HomePage
from Test3.pages.careers_page import CareersPage
from Test3.pages.qa_jobs_page import QAJobsPage
from Test3.utilities.browser_factory import BrowserFactory


class TestCareersPage(unittest.TestCase):

    def setUp(self):
        browser_name = "chrome"  # Change to "firefox" to run in Firefox
        self.driver = BrowserFactory(browser_name).get_driver()
        self.driver.maximize_window()
        self.home_page = HomePage(self.driver)
        self.careers_page = CareersPage(self.driver)
        self.qa_jobs_page = QAJobsPage(self.driver)

    def test_careers_flow(self):
        try:
            # Step 1: Visit https://useinsider.com/ and check Insider home page
            self.home_page.open_url("https://useinsider.com/")
            self.assertTrue(self.home_page.is_home_page_opened(), "Home page is not opened")

            # Step 2: Navigate to Careers Page and check blocks
            self.home_page.navigate_to_careers()
            self.assertTrue(self.careers_page.are_career_blocks_visible(), "Career page blocks not visible")

            # Step 3 & 4: Go to Quality Assurance Jobs and perform filtering
            self.careers_page.navigate_to_qa_jobs()
            self.qa_jobs_page.scroll_to_qa_btn()
            self.qa_jobs_page.click(self.qa_jobs_page.SEE_ALL_JOBS_BTN)
            self.qa_jobs_page.scroll_to_location_filter()
            # Apply filters for Istanbul and Quality Assurance
            self.qa_jobs_page.filter_jobs(location="Istanbul, Turkey", department="Quality Assurance")

            self.qa_jobs_page.are_filtered_jobs_present()

            # Step 5: Click "View Role" and check moving to another page
            self.qa_jobs_page.click_view_role()
             # Check the URL to confirm redirection
            self.assertIn("jobs.lever.co", self.driver.current_url, "Did not redirect to Lever Application form")



        except Exception as e:
            print(f"Test failed: {e}")
            self.qa_jobs_page.take_screenshot("test_careers_flow")
            raise  # Re-raise the exception so the test fails correctly

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()