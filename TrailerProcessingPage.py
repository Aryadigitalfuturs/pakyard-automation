from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class TrailerProcessingPage:
    def __init__(self, driver):
        self.driver = driver

    def is_loaded(self):
        return WebDriverWait(self.driver, 20).until(EC.url_contains("trailer-processing"))

    def click_view_button(self):
        try:
            print("Clicking 'Today' filter button to ensure data is loaded.")
            today_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Today']"))
            )
            self.driver.execute_script("arguments[0].click();", today_button)
            time.sleep(5)  # Allow more time for the table to refresh after filtering
        except Exception as e:
            print(f"Could not click 'Today' button, proceeding anyway. Error: {e}")

        # Using the absolute XPath provided by the user.
        view_button_xpath = "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[8]/div/button[1]"
        try:
            print(f"Waiting for view button with XPath: {view_button_xpath}")
            # Wait for the element to be clickable.
            view_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, view_button_xpath))
            )
            print("View button found. Clicking...")
            # Scroll into view and click with JavaScript for reliability
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", view_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", view_button)
            print("Clicked view button successfully.")
        except Exception as e:
            print(f"Could not find or click the view button with the provided XPath. Error: {e}")
            self.driver.save_screenshot("view_button_click_fail.png")
            # Re-raise the exception to ensure the test fails here and does not proceed.
            raise 

    def click_start_inspection(self):
        start_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Start Inspection')]")))
        start_button.click()
    
    def enter_inspector_name(self, inspector_name):
        inspector_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, "nameOfInspector")))
        inspector_input.clear()
        inspector_input.send_keys(inspector_name)

    def click_yes_for_all_questions(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Yes']")))
        except TimeoutException:
            print("No 'Yes' buttons found.")

        yes_buttons = self.driver.find_elements(By.XPATH, "//button[normalize-space()='Yes']")
        for btn in yes_buttons:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", btn)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", btn)

    def check_and_upload_photo(self, file_path):
        time.sleep(2)
        elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Please add a photo')]")
        if len(elements) > 0:
            print("Question asking for photo found. Uploading...")
            file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
            for input_field in file_inputs:
                try:
                    input_field.send_keys(file_path)
                    print("Photo uploaded successfully.")
                    time.sleep(2)
                except Exception as e:
                    print(f"Error uploading photo: {e}")

    def click_save_inspection(self):
        save_button_xpath = "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/form/div[3]/div[2]/div[2]/button"
        save_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, save_button_xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", save_button)

    def click_start_loading(self):
        start_loading_button_xpath = "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/form/div[3]/div[1]/div/button"
        start_loading_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, start_loading_button_xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_loading_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", start_loading_button)

    def enter_loader_name(self, loader_name):
        loader_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/form/div[1]/div[1]//input"))
        )
        loader_input.clear()
        loader_input.send_keys(loader_name)

    def click_confirm_checkbox(self):
        checkbox_xpath = "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/form/div[3]/div[2]/div[1]/div[3]/div/button"
        checkbox = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", checkbox)

    def click_mark_as_complete(self):
        mark_complete_xpath = "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/form/div[3]/div[2]/div[2]/button"
        mark_complete_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, mark_complete_xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mark_complete_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", mark_complete_button)
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Success') or contains(text(), 'successfully')]")))

    def click_trailer_processing_nav(self):
        nav_xpath = "/html/body/div[2]/div[1]/div[2]/a[9]"
        nav_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, nav_xpath))
        )
        nav_button.click()
