from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

class TrailerProcessingObPage:
    def __init__(self, driver):
        self.driver = driver

    def is_loaded(self):
        return WebDriverWait(self.driver, 20).until(EC.url_contains("trailer-processing"))

    def click_view_button(self, dock_door=None):
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
        view_button_xpath = "/html/body/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr[1]/td[12]/div/button[1]"
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

    def assign_dock_door(self, dock_door):
        print(f"Assigning dock door: {dock_door}")
        # Click Change Door (Edit icon)
        change_door_xpath = "/html/body/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr[1]/td[9]/div/button[2]"
        change_door_btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, change_door_xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", change_door_btn)
        self.driver.execute_script("arguments[0].click();", change_door_btn)
        time.sleep(2)

        # Click Dropdown Trigger
        dropdown_xpath = "/html/body/div[5]/div[1]/div[2]/button"
        dropdown_btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
        self.driver.execute_script("arguments[0].click();", dropdown_btn)
        time.sleep(1)

        # Select Dock Door Option
        option_xpath = f"//li[contains(., '{dock_door}')] | //div[@role='option'][contains(., '{dock_door}')]"
        option_btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        self.driver.execute_script("arguments[0].click();", option_btn)
        time.sleep(1)

        # Click Confirm Change
        confirm_xpath = "//button[contains(., 'Change Door')]"
        confirm_btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, confirm_xpath)))
        self.driver.execute_script("arguments[0].click();", confirm_btn)
        time.sleep(2)

    def click_start_inspection(self):
        start_button_xpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[1]/div/div[2]/button[1]"
        start_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, start_button_xpath)))
        start_button.click()
    
    def enter_inspector_name(self, inspector_name):
        inspector_input_xpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[1]/div[1]/input"
        inspector_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, inspector_input_xpath)))
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
        pass
        # time.sleep(2)
        # elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Please add a photo')]")
        # if len(elements) > 0:
        #     print("Question asking for photo found. Uploading...")
        #     file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
        #     for input_field in file_inputs:
        #         try:
        #             input_field.send_keys(file_path)
        #             print("Photo uploaded successfully.")
        #             time.sleep(2)
        #         except Exception as e:
        #             print(f"Error uploading photo: {e}")

    def click_save_inspection(self):
        save_button_xpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[2]/div[2]/button"
        save_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, save_button_xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", save_button)

    def click_start_loading(self):
        start_loading_button_xpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[1]/button"
        start_loading_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, start_loading_button_xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_loading_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", start_loading_button)
        
        # Click Skip verification
        try:
            skip_verification_xpath = "//button[contains(., 'Skip verification')] | //button[contains(., 'Skip')] | /html/body/div[5]/div[3]/button[2]"
            skip_verification_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, skip_verification_xpath))
            )
            self.driver.execute_script("arguments[0].click();", skip_verification_btn)
            time.sleep(2)
        except Exception as e:
            print(f"Skip verification button not found or not needed: {e}")

        # Click Skip and continue
        try:
            skip_continue_xpath = "//button[contains(., 'Skip and continue')] | /html/body/div[7]/div[4]/button[2]"
            skip_continue_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, skip_continue_xpath))
            )
            self.driver.execute_script("arguments[0].click();", skip_continue_btn)
            time.sleep(2)
        except Exception as e:
            print(f"Skip and continue button not found or not needed: {e}")

        # Click Confirm Start
        try:
            confirm_start_xpath = "//button[contains(., 'Confirm Start')] | //button[contains(., 'Confirm')] | /html/body/div[5]/div[3]/button[2]"
            confirm_start_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, confirm_start_xpath))
            )
            self.driver.execute_script("arguments[0].click();", confirm_start_btn)
            time.sleep(2)
        except Exception as e:
            print(f"Confirm Start button not found or not needed: {e}")

    def enter_loader_name(self, loader_name):
        loader_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[1]/div[1]/input"))
        )
        loader_input.clear()
        loader_input.send_keys(loader_name)

    def enter_line_count(self, count):
        line_count_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[2]/div[1]/input"))
        )
        line_count_input.clear()
        line_count_input.send_keys(count)

    def enter_pallet_quantity(self, quantity):
        pallet_quantity_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[2]/div[2]/input"))
        )
        pallet_quantity_input.clear()
        pallet_quantity_input.send_keys(quantity)

    def click_confirm_checkbox(self):
        checkbox_xpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[2]/div[1]/div[3]/div/button"
        checkbox = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", checkbox)

    def click_mark_as_complete(self):
        mark_complete_xpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[3]/div/button"
        mark_complete_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, mark_complete_xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mark_complete_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", mark_complete_button)
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Success') or contains(text(), 'successfully')]")))

    def click_verify_seal(self):
        # Try finding the button by text first, as absolute XPaths are fragile
        xpath_options = [
            "//button[contains(., 'Verify Seal')]",
            "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/form/div[3]/div[1]/div/div/button"
        ]
        
        for xpath in xpath_options:
            try:
                verify_seal_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", verify_seal_btn)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", verify_seal_btn)
                return
            except TimeoutException:
                continue
        raise Exception("Could not find 'Verify Seal' button")

    def enter_seal_number(self, seal_number):
        # Expanded XPath to find the input even if role='dialog' is missing or structure changed
        seal_input_xpath = "//div[@role='dialog']//input[not(@type='file') and not(@type='hidden')] | //div[contains(@class, 'fixed')]//input[not(@type='file') and not(@type='hidden')]"
        seal_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, seal_input_xpath))
        )
        seal_input.clear()
        seal_input.send_keys(seal_number)

    def upload_seal_image(self, file_path):
        upload_input_xpath = "//div[@role='dialog']//input[@type='file'] | //div[contains(@class, 'fixed')]//input[@type='file']"
        upload_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, upload_input_xpath))
        )
        upload_input.send_keys(file_path)

    def click_save_seal_verification(self):
        save_xpath = "//div[@role='dialog']//button[contains(., 'Verify') or contains(., 'VERIFY')] | //div[contains(@class, 'fixed')]//button[contains(., 'Verify') or contains(., 'VERIFY')]"
        save_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, save_xpath))
        )
        self.driver.execute_script("arguments[0].click();", save_btn)

    def click_start_seal_verification(self):
        time.sleep(2) # Allow modal to close and main page to settle
        xpath_options = [
            "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[1]/div[1]/div/button", 
            "//button[contains(., 'Start Seal Verification')]",
            "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/form/div[3]/div/div[1]/div/button",
            "//button[contains(text(), 'Start Seal')]"
        ]
        for xpath in xpath_options:
            try:
                # Use visibility + clickability check
                start_seal_btn = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_seal_btn)
                time.sleep(2) # Give it a moment to stabilize
                try:
                    start_seal_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", start_seal_btn)
                print("Clicked Start Seal Verification.")
                return
            except (TimeoutException, StaleElementReferenceException):
                continue
        raise Exception("Could not find 'Start Seal Verification' button")

    def click_final_yes(self):
        print("Clicking final 'Yes' for seal verification...")
        xpath_options = [
            "//button[normalize-space()='Yes']",
            "//div[contains(@class, 'seal-verification')]//button[contains(., 'Yes')]",
            "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[1]/div[2]/div[2]/div/div/div[1]/button"
        ]
        for xpath in xpath_options:
            try:
                yes_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", yes_btn)
                time.sleep(1)
                # Fallback to JS click if normal click fails
                self.driver.execute_script("arguments[0].click();", yes_btn)
                return
            except:
                continue
        raise Exception("Could not find final 'Yes' button for seal verification.")

    def click_final_mark_complete(self):
        print("Clicking final 'Mark as Complete' button...")
        xpath_options = [
            "//button[contains(., 'Mark as Complete')]",
            "//button[contains(., 'Complete')]",
            "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[1]/div[2]/div[3]/button"
        ]
        for xpath in xpath_options:
            try:
                complete_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", complete_btn)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", complete_btn)
                return
            except:
                continue
        raise Exception("Could not find final 'Mark as Complete' button.")

    def click_trailer_processing_nav(self):
        # Use a robust locator to navigate back to processing list
        nav_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/trailer-processing')]"))
        )
        nav_button.click()

    def click_start_bol_creation(self):
        print("Clicking 'Start BOL Creation' button...")
        xpath_options = [
            "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[1]/div[1]/div/button[2]",
            "//button[contains(., 'Start BOL')]",
        ]
        for xpath in xpath_options:
            try:
                btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].click();", btn)
                return
            except:
                continue
        raise Exception("Could not find 'Start BOL Creation' button.")

    def click_complete_checkout_main(self):
        print("Clicking 'Complete Check Out' button...")
        xpath_options = [
            "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[1]/div[1]/div/button[2]",
            "//button[contains(., 'Complete Check Out')]",
            "//button[contains(., 'Complete Checkout')]",
            "//form//button[contains(., 'Complete')]"
        ]
        for xpath in xpath_options:
            try:
                btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                time.sleep(1)
                try:
                    btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", btn)
                print("Clicked 'Complete Check Out' successfully.")
                return
            except:
                continue
        raise Exception("Could not find 'Complete Check Out' button.")

    def click_continue_modal_button(self):
        print("Clicking 'Continue' button on modal...")
        xpath = "/html/body/div[5]/div[3]/button[2]"
        try:
            btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].click();", btn)
            print("Clicked 'Continue' successfully.")
        except Exception as e:
            print(f"Error clicking Continue button: {e}")
            raise

    def click_preview_bol(self):
        print("Attempting to click Preview BOL button...")
        # Prioritizing the specific XPath provided by the user
        locators = [
            (By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div[1]/div[2]/div/button"),
            (By.XPATH, "//button[contains(normalize-space(), 'Preview BOL')]"),
            (By.XPATH, "//button[contains(., 'Preview')]")
        ]

        for attempt in range(3):
            for by, value in locators:
                try:
                    btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((by, value)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(1)
                    
                    # Try regular click first, then fallback to JS click
                    try:
                        btn.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", btn)
                    
                    print("Preview BOL button clicked successfully.")
                    return
                except (TimeoutException, StaleElementReferenceException):
                    continue
            print(f"Retrying Preview BOL click... (Attempt {attempt + 1}/3)")
            time.sleep(2)
            
        raise Exception("Failed to click Preview BOL button after multiple attempts and locators.")

    def scroll_to_bottom(self):
        print("Scrolling to the bottom of the page...")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    def wait_for_save_enabled(self):
        print("Waiting for Save button to be enabled...")
        save_xpath = "//button[contains(., 'Save')]"
        try:
            WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, save_xpath)))
            print("Save button is now enabled.")
            return True
        except TimeoutException:
            print("Save button did not become clickable within 60s. Checking if Preview is already available...")
            if self.driver.find_elements(By.XPATH, "//button[contains(., 'Preview BOL')]"):
                print("Preview BOL button detected, skipping Save wait.")
                return False
            else:
                raise

    def click_save_bol(self):
        save_xpath = "//button[contains(., 'Save')]"
        btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, save_xpath)))
        self.driver.execute_script("arguments[0].click();", btn)
        # Verification for BOL (Handles both PAKAPPs and standard success messages)
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'BOL Generated Successfully') or contains(text(), 'BOL Submitted Successfully')]")))

    def click_go_to_checkout(self):
        xpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div/div[2]/div/div/button"
        print("Waiting for 'Go to Checkout Page' button...")
        btn = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)
        print("Clicked 'Go to Checkout Page' successfully.")

    def click_start_checkout_final(self):
        xpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div/button"
        print("Waiting for 'Start CheckOut' button...")
        btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)
        print("Clicked 'Start CheckOut' successfully.")

    def click_complete_checkout_final(self):
        xpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div[2]/form/div[3]/div/div/button"
        print("Waiting for 'Complete Checkout' button...")
        btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)
        print("Clicked 'Complete Checkout' successfully.")
