from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.sso_button = (By.XPATH, "//button[contains(., 'SSO Login with Microsoft')] | //a[contains(., 'SSO Login with Microsoft')]")

    def load(self):
        self.driver.get("https://dev.pakyard.drinkpak.com/")

    def click_sso(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.sso_button)).click()