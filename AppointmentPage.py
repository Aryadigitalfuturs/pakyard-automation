from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time

class AppointmentPage:
    def __init__(self, driver):
        self.driver = driver
        self.customer_dropdown = (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/button")
        self.plus_icon = (By.XPATH, "(//button[.//svg][not(ancestor::tbody)])[last()]")

    def is_loaded(self):
        # Verify that the URL contains 'appointment' or check for a specific element
        return WebDriverWait(self.driver, 20).until(EC.url_contains("appointment"))
    time.sleep(2)
    

    def select_customer(self, customer_name):
        wait = WebDriverWait(self.driver, 20)
        element = wait.until(EC.element_to_be_clickable(self.customer_dropdown))
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(2)
        option = (By.XPATH, f"//li[contains(., '{customer_name}')] | //div[@role='option'][contains(., '{customer_name}')]")
        option_element = wait.until(EC.element_to_be_clickable(option))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", option_element)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", option_element)

    def select_time_slot(self, time_slot):
        # Find the row containing the time text.
        # Based on the specific XPath provided previously, the '+' icon is in the 3rd column (td[3]).
        # Handle potential time format mismatch (e.g. 12.00 vs 12:00)
        time_slot_colon = time_slot.replace('.', ':')
        
        # Find row where the first column contains the time, then target the div in the 3rd column
        xpath = f"//tr[td[1][contains(normalize-space(.), '{time_slot}') or contains(normalize-space(.), '{time_slot_colon}')]]/td[3]//*[local-name()='svg']"
        
        # Wait for the element to be present
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        
        # Scroll the element into view and click using JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
        time.sleep(1)
        ActionChains(self.driver).move_to_element(element).click().perform()

    def click_plus_icon(self):
        element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.plus_icon))
        self.driver.execute_script("arguments[0].click();", element)

    def select_carrier(self, carrier_name):
        # Use the specific XPath provided for the carrier dropdown button
        carrier_dropdown = (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div[1]/div/table/tbody/tr[4]/td[3]/div/div/div[2]/div[2]/form/div[1]/div[3]/button")
        wait = WebDriverWait(self.driver, 20)
        element = wait.until(EC.element_to_be_clickable(carrier_dropdown))
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(2)
        option = (By.XPATH, f"//li[contains(., '{carrier_name}')] | //div[@role='option'][contains(., '{carrier_name}')]")
        option_element = wait.until(EC.element_to_be_clickable(option))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", option_element)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", option_element)

    def click_save(self):
        save_button = (By.XPATH, "//button[@type='submit' and contains(., 'SAVE')]")
        element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(save_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", element)

        try:
            confirm_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Confirm Schedule')]")))
            self.driver.execute_script("arguments[0].click();", confirm_button)
            time.sleep(2)
            print("Clicked 'Confirm Schedule' on warning.")
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Success') or contains(text(), 'successfully')]")))
        except TimeoutException:
            pass

    def enter_contact_name(self, contact_name):
        contact_input = (By.ID, "contact")
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(contact_input))
        element.clear()
        element.send_keys(contact_name)

    def enter_contact_number(self, contact_number):
        phone_input = (By.ID, "phone")
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(phone_input))
        element.clear()
        element.send_keys(contact_number)

    def enter_email(self, email):
        email_input = (By.ID, "email")
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(email_input))
        element.clear()
        element.send_keys(email)

    def enter_receipt_id(self, receipt_id):
        receipt_input = (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div[1]/div/table/tbody/tr[4]/td[3]/div/div/div[2]/div[2]/form/div[1]/div[4]/input")
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(receipt_input))
        element.clear()
        element.send_keys(receipt_id)

    def select_order_type(self, order_type):
        # Use the specific XPath provided for the order type dropdown button
        order_type_dropdown = (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div[1]/div/table/tbody/tr[4]/td[3]/div/div/div[2]/div[2]/form/div[1]/div[5]/button")
        wait = WebDriverWait(self.driver, 20)
        element = wait.until(EC.element_to_be_clickable(order_type_dropdown))
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(2)
        option = (By.XPATH, f"//li[contains(., '{order_type}')] | //div[@role='option'][contains(., '{order_type}')] | //span[contains(., '{order_type}')] | //div[contains(text(), '{order_type}')]")
        option_element = wait.until(EC.element_to_be_clickable(option))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", option_element)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", option_element)