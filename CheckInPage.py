from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class CheckInPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://dev.pakyard.drinkpak.com/check-in/code"
        self.confirmation_display = (By.XPATH, "//div[contains(@class, 'bg-gray-100')]//span")

    def load(self):
        self.driver.get(self.url)

    def enter_code(self, code):
        # Target the specific display container using the inner span's unique color class
        xpath = "//div[.//span[contains(@class, 'text-[#2562a8]')]]"
        container = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        container.click()
        time.sleep(1)
        ActionChains(self.driver).send_keys(code).perform()
        time.sleep(3)

    def click_confirm(self):
        confirm_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'CONFIRM')]")))
        confirm_button.click()

    def enter_driver_name(self, driver_name):
        driver_name_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Full Name']")))
        driver_name_input.clear()
        driver_name_input.send_keys(driver_name)

    def enter_driver_cell(self, driver_cell):
        cell_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, "driverCell")))
        cell_input.clear()
        cell_input.send_keys(driver_cell)

    def enter_license_number(self, license_number):
        license_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, "licenseNumber")))
        license_input.clear()
        license_input.send_keys(license_number)

    def select_license_state(self, state):
        dropdown = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Select License State')]")))
        dropdown.click()
        option = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//div[@role='option'][contains(., '{state}')] | //span[contains(text(), '{state}')]")))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", option)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", option)

    def enter_tractor_number(self, tractor_number):
        tractor_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, "tractorNumber")))
        tractor_input.clear()
        tractor_input.send_keys(tractor_number)

    def select_trailer_type(self, trailer_type):
        dropdown = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Select Trailer Type')]")))
        dropdown.click()
        option = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//div[@role='option'][contains(., '{trailer_type}')] | //span[contains(text(), '{trailer_type}')]")))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", option)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", option)

    def enter_trailer_number(self, trailer_number):
        trailer_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, "trailerNumber")))
        trailer_input.clear()
        trailer_input.send_keys(trailer_number)

    def upload_document(self, file_path):
        file_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "bol-upload")))
        file_input.send_keys(file_path)
        time.sleep(2)

    def click_finish(self):
        xpath = "//button[contains(., 'FINISH')]"
        finish_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", finish_button)
        time.sleep(1)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].click();", finish_button)
        time.sleep(2)