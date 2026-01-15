from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.dashboard_header = (By.XPATH, "//h1[contains(., 'Welcome to the PAKYARD')] | //h1[contains(., 'Dashboard')]")
        self.appointment_button = (By.XPATH, "//button[contains(., 'Appointments')] | //a[contains(., 'Appointments')]")
        self.trailer_processing_link = (By.XPATH, "//a[contains(@href, '/trailer-processing')]")

    def is_dashboard_displayed(self):
        return WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(self.dashboard_header)).is_displayed()

    def click_appointment(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.appointment_button)).click()

    def click_trailer_processing(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.trailer_processing_link)).click()