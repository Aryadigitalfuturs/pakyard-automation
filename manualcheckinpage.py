from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class ManualCheckInPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver_name_input = (By.XPATH, "//input[contains(@placeholder, 'Name')] | //form//div[1]//input")
        self.trailer_number_input = (By.XPATH, "//input[contains(@placeholder, 'Trailer')] | //form//div[3]//input")
        self.trailer_type_dropdown = (By.XPATH, "//form//div[7]//button | /html/body/div[5]/form/div[1]/div[7]/button")
        self.carrier_dropdown = (By.XPATH, "//form//div[8]//button | /html/body/div[5]/form/div[1]/div[8]/button")
        self.ontime_comment_dropdown = (By.XPATH, "//form//div[9]//button | /html/body/div[5]/form/div[1]/div[9]/button")
        self.confirm_checkin_button = (By.XPATH, "//button[contains(., 'Confirm Check In')] | //button[contains(., 'Confirm')]")
        self.dock_door_dropdown = (By.XPATH, "/html/body/div[5]/div/div[2]/div/button | //div[contains(@class, 'modal')]//div[2]/div/button")
        self.assign_dock_door_button = (By.XPATH, "/html/body/div[5]/div/div[2]/div/button[2] | //button[contains(., 'Assign')]")
        self.done_button = (By.XPATH, "/html/body/div[5]/div/button | //button[contains(., 'Done')] | //div[contains(@class, 'modal')]//button")

    def click_trailer_icon(self, shipment_id):
        print(f"Waiting for Trailer icon for Shipment ID: {shipment_id}...")
        
        # Ensure the row is present, refresh if needed
        row_xpath = f"//tr[contains(., '{shipment_id}')]"
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, row_xpath)))
        except:
            print(f"Row for {shipment_id} not found. Refreshing page...")
            self.driver.refresh()
            time.sleep(5)
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, row_xpath)))
            except:
                raise Exception(f"Row for Shipment ID {shipment_id} not found even after refresh.")

        # Scroll row into view and allow buttons to render
        row_element = self.driver.find_element(By.XPATH, row_xpath)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row_element)
        time.sleep(2)

        # Try multiple strategies to find the trailer/check-in icon button
        strategies = [
            f"//tr[contains(., '{shipment_id}')]/td[2]/div/div/div[2]/span[2]/button",
            f"//tr[contains(., '{shipment_id}')]/td[2]/div/div[2]/div[2]/span[2]/button",
            f"//tr[contains(., '{shipment_id}')]//button[.//svg]", # Button containing an SVG icon
            f"//tr[contains(., '{shipment_id}')]//span[contains(@class, 'button')]//button",
            f"//tr[contains(., '{shipment_id}')]//td[2]//button[last()]",
            f"//tr[contains(., '{shipment_id}')]//button[contains(@class, 'checkin')]",
            f"(//tr[contains(., '{shipment_id}')]//button)[2]",
            f"(//tr[contains(., '{shipment_id}')]//button)[last()]",
            f"//tr[contains(., '{shipment_id}')]//button" # Fallback: any button in that row
        ]

        for xpath in strategies:
            try:
                element = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                
                # Use ActionChains to move to element and click for better reliability
                try:
                    ActionChains(self.driver).move_to_element(element).click().perform()
                except:
                    try:
                        element.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", element)
                time.sleep(2)
                
                # Verify form or page loaded by checking for the driver name input field
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.driver_name_input))
                print(f"Clicked Trailer icon for Shipment ID: {shipment_id}.")
                return
            except:
                continue
        
        raise Exception(f"Could not find clickable Trailer icon for Shipment ID: {shipment_id}")

    def enter_driver_name(self, driver_name):
        print(f"Entering Driver Name: {driver_name}")
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.driver_name_input)
        )
        try:
            element.clear()
        except:
            self.driver.execute_script("arguments[0].value = '';", element)
        element.send_keys(driver_name)
        time.sleep(1)

    def enter_trailer_number(self, trailer_number):
        print(f"Entering Trailer Number: {trailer_number}")
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.trailer_number_input)
        )
        try:
            element.clear()
        except:
            self.driver.execute_script("arguments[0].value = '';", element)
        element.send_keys(trailer_number)
        time.sleep(1)

    def select_trailer_type(self, trailer_type):
        print(f"Selecting Trailer Type: {trailer_type}")
        self._select_dropdown_option(self.trailer_type_dropdown, trailer_type)

    def select_carrier(self, carrier_name):
        print(f"Selecting Carrier: {carrier_name}")
        self._select_dropdown_option(self.carrier_dropdown, carrier_name)

    def select_ontime_comment(self, comment):
        print(f"Selecting On-Time Comment: {comment}")
        self._select_dropdown_option(self.ontime_comment_dropdown, comment)

    def select_dock_door(self, dock_door):
        print(f"Selecting Dock Door: {dock_door}")
        self._select_dropdown_option(self.dock_door_dropdown, dock_door)

    def click_assign_dock_door(self):
        print("Clicking Assign Dock Door button...")
        button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.assign_dock_door_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", button)
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

    def _select_dropdown_option(self, dropdown_locator, option_text):
        """Internal helper to handle dropdown clicks and robust option selection."""
        dropdown = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(dropdown_locator)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", dropdown)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", dropdown)
        time.sleep(1)
        
        lower_text = option_text.lower()
        strategies = [
            f"//li[contains(normalize-space(.), '{option_text}')] | //div[@role='option'][contains(normalize-space(.), '{option_text}')]",
            f"//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{lower_text}')]"
        ]

        for xpath in strategies:
            try:
                option = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].click();", option)
                time.sleep(1)
                return
            except:
                continue
        
        raise Exception(f"Option '{option_text}' not found in dropdown.")

    def click_confirm_checkin(self):
        print("Clicking Confirm Check-in button...")
        button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.confirm_checkin_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", button)
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(5)

    def click_done(self):
        print("Clicking Done button...")
        button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.done_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", button)
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(2)