from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LogoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.logout_button = (By.XPATH, "//button[contains(., 'Logout')]")
        self.confirm_logout_button = (By.XPATH, "//button[contains(@class, 'bg-destructive') and contains(., 'Logout')]")

    def click_logout(self):
        element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.logout_button))
        self.driver.execute_script("arguments[0].click();", element)

    def click_confirm_logout(self):
        element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.confirm_logout_button))
        self.driver.execute_script("arguments[0].click();", element)