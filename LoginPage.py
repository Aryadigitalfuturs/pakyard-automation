from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Using the specific XPath provided, with text-based fallbacks for reliability
        self.sso_xpath = "/html/body/main/div/div[2]/div[2]/div[2]/form/button"
        self.sso_fallback = "//button[contains(., 'Microsoft')] | //button[contains(., 'SSO')] | //button[@type='submit']"

    def load(self):
        self.driver.get("https://dev.pakyard.drinkpak.com/")

    def click_sso(self):
        print(f"Attempting to click SSO button using: {self.sso_xpath}")
        try:
            # Try the specific absolute XPath first
            btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.sso_xpath)))
        except:
            print("Absolute XPath failed, trying robust text-based locator...")
            btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.sso_fallback)))
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        try:
            btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", btn)