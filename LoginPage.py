from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.sso_button = (By.XPATH, "/html/body/main/div/div[2]/div[2]/div[2]/form/button")

    def load(self):
        self.driver.get("https://dev.pakyard.drinkpak.com/")

    def click_sso(self):
        element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.sso_button))
        self.driver.execute_script("arguments[0].click();", element)