from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    def click_checkout_driver(self):
        # XPath provided for the checkout driver button
        checkout_button_xpath = "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[1]/button[2]"
        scan_driver_xpath = "/html/body/div[5]/div/div/button"
        allow_camera_xpath = "/html/body/div[5]/div/div/div/button"
        try:
            print(f"Waiting for Checkout Driver button with XPath: {checkout_button_xpath}")
            checkout_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, checkout_button_xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", checkout_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", checkout_button)
            print("Clicked Checkout Driver button.")
            
            # Click Scan Driver button
            print(f"Waiting for Scan Driver button with XPath: {scan_driver_xpath}")
            scan_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, scan_driver_xpath))
            )
            self.driver.execute_script("arguments[0].click();", scan_button)
            print("Clicked Scan Driver button.")
            
            # Click Allow Camera Access button
            try:
                print(f"Waiting for Allow Camera Access button with XPath: {allow_camera_xpath}")
                allow_camera_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, allow_camera_xpath))
                )
                self.driver.execute_script("arguments[0].click();", allow_camera_button)
                print("Clicked Allow Camera Access button.")
            except TimeoutException:
                print("Allow Camera Access button not found (possibly auto-granted). Proceeding.")
            
            # Wait for success message
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Checkout process started') or contains(text(), 'successfully')]")))
            print("Success message displayed.")
        except Exception as e:
            print(f"Error clicking Checkout Driver button: {e}")
            self.driver.save_screenshot("checkout_driver_fail.png")
            raise

    def click_complete_checkout(self):
        complete_checkout_xpath = "/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/form/div[3]/div[5]/div/button"
        try:
            print(f"Waiting for Complete Checkout button with XPath: {complete_checkout_xpath}")
            complete_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, complete_checkout_xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", complete_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", complete_button)
            print("Clicked Complete Checkout button.")
            
            # Wait for success message
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Driver Checkout')]")))
            print("Success message 'Driver Checkout' displayed.")
        except Exception as e:
            print(f"Error clicking Complete Checkout button: {e}")
            self.driver.save_screenshot("complete_checkout_fail.png")
            raise