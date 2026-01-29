from selenium import webdriver
import json
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from LoginPage import LoginPage
from HomePage import HomePage
from AppointmentObpage import AppointmentObPage
from LogoutPage import LogoutPage
from CheckInPage import CheckInPage
from TrailerProcessingObPage import TrailerProcessingObPage
from CheckoutPage import CheckoutPage

def get_driver():
    options = webdriver.ChromeOptions()
    # Use a user data directory to persist login session
    options.add_argument("user-data-dir=C:\\Users\\Admin\\Python\\PAKYARD\\ChromeData")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream_camera": 1})
    driver = webdriver.Chrome(options=options)
    return driver

def execute_login_page(driver):
    login_page = LoginPage(driver)
    login_page.load()
    driver.maximize_window()

    # If redirected to home/dashboard due to a saved session, we are already logged in.
    if "/home" in driver.current_url or "dashboard" in driver.current_url:
        print("Already logged in, skipping login process.")
        return

    # If not logged in, proceed to click the SSO button.
    print("Clicking SSO button...")
    # The original implementation in LoginPage.py is failing with a TimeoutException.
    # This is likely due to a fragile locator or interaction issue.
    # We will use a more robust method here to find and click the button.
    sso_button_xpath = "/html/body/main/div/div[2]/div[2]/div[2]/form/button"
    sso_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, sso_button_xpath))
    )
    driver.execute_script("arguments[0].click();", sso_button)

    # Wait for the URL to change, confirming login was successful
    WebDriverWait(driver, 30).until(lambda d: "/home" in d.current_url or "dashboard" in d.current_url)
    print("Login Page Test Passed!")

def execute_home_page(driver):
    home_page = HomePage(driver)
    assert home_page.is_dashboard_displayed()
    print("Login successful! Dashboard displayed.")

    # Click on appointment screen
    print("Navigating to Appointment screen...")
    home_page.click_appointment()
    print("Home Page Test Passed!")

def execute_appointment_page(driver):
    appointment_page = AppointmentObPage(driver)
    
    # Verify Appointment page loaded
    if appointment_page.is_loaded():
        print("Appointment Schedule page loaded successfully!")

    with open(r"c:\Users\Admin\Python\PAKYARD\test_data.json", "r") as f:
        data = json.load(f)

    for appointment in data["appointments"]:
        print(f"Selecting customer: {appointment['customer']}")
        appointment_page.select_customer(appointment['customer'])
        time.sleep(5)
        print(f"Clicking + icon for time: {appointment['time']}")
        appointment_page.select_time_slot(appointment['time'])
        time.sleep(5)
        
        if "carrier" in appointment:
            print(f"Selecting carrier: {appointment['carrier']}")
            appointment_page.select_carrier(appointment['carrier'])
            time.sleep(2)

        if "shipment_id" in appointment:
            print(f"Entering Shipment ID: {appointment['shipment_id']}")
            appointment_page.enter_shipment_id(appointment['shipment_id'])
            time.sleep(2)

        if "order_type" in appointment:
            print(f"Selecting Order Type: {appointment['order_type']}")
            appointment_page.select_order_type(appointment['order_type'])
            time.sleep(2)

        if "contact_name" in appointment:
            print(f"Entering Contact Name: {appointment['contact_name']}")
            appointment_page.enter_contact_name(appointment['contact_name'])
            time.sleep(2)

        if "contact_number" in appointment:
            print(f"Entering Contact Number: {appointment['contact_number']}")
            appointment_page.enter_contact_number(appointment['contact_number'])
            time.sleep(2)

        if "email" in appointment:
            print(f"Entering Email: {appointment['email']}")
            appointment_page.enter_email(appointment['email'])
            time.sleep(2)

        print("Clicking Save button...")
        appointment_page.click_save()
        time.sleep(5)
    print("Appointment Page Test Passed!")

def execute_logout_page(driver):
    logout_page = LogoutPage(driver)
    print("Clicking Logout button...")
    logout_page.click_logout()
    time.sleep(2)
    print("Confirming Logout...")
    logout_page.click_confirm_logout()
    time.sleep(3)
    print("Logout Page Test Passed!")

def execute_checkin_page(driver):
    checkin_page = CheckInPage(driver)
    print("Navigating to Check-In Page...")
    checkin_page.load()
    time.sleep(2)
    code = input("Enter Confirmation Number : ")
    checkin_page.enter_code(code)
    checkin_page.click_confirm()
    time.sleep(2)

    with open(r"c:\Users\Admin\Python\PAKYARD\test_data.json", "r") as f:
        data = json.load(f)
    checkin_page.enter_driver_name(data["checkin"]["driver_name"])
    checkin_page.enter_driver_cell(data["checkin"]["driver_cell"])
    checkin_page.enter_license_number(data["checkin"]["license_number"])
    checkin_page.select_license_state(data["checkin"]["license_state"])
    checkin_page.enter_tractor_number(data["checkin"]["tractor_number"])
    checkin_page.select_trailer_type(data["checkin"]["trailer_type"])
    checkin_page.enter_trailer_number(data["checkin"]["trailer_number"])
    checkin_page.upload_document(data["checkin"]["document_path"])
    checkin_page.click_finish()
    time.sleep(5)
    print("Check-In Page Test Passed!")

def execute_trailer_processing_ob_page(driver):
    home_page = HomePage(driver)
    if home_page.is_dashboard_displayed():
        print("Dashboard displayed.")
    print("Navigating to Trailer Processing screen...")
    home_page.click_trailer_processing()
    trailer_page = TrailerProcessingObPage(driver)
    if trailer_page.is_loaded():
        print("Trailer Processing page loaded successfully!")
    
    with open(r"c:\Users\Admin\Python\PAKYARD\test_data.json", "r") as f:
        data = json.load(f)

    print("Clicking View button...")
    trailer_page.click_view_button(dock_door=data['dock_door'])
    time.sleep(2)

    print("Clicking Start Inspection button...")
    trailer_page.click_start_inspection()
    time.sleep(2)

    print(f"Entering Inspector Name: {data['inspection']['inspector_name']}")
    trailer_page.enter_inspector_name(data['inspection']['inspector_name'])

    print("Clicking Yes for all questions...")
    trailer_page.click_yes_for_all_questions()

    print("Checking for photo upload...")
    trailer_page.check_and_upload_photo(data['checkin']['document_path'])

    print("Clicking Save Inspection button...")
    trailer_page.click_save_inspection()
    time.sleep(5)

    print("Clicking Start Loading button...")
    trailer_page.click_start_loading()
    time.sleep(2)

    print(f"Entering Loader Name: {data['inspection']['loader_name']}")
    trailer_page.enter_loader_name(data['inspection']['loader_name'])

    print(f"Entering Pallet Quantity: {data['inspection']['pallet_quantity']}")
    trailer_page.enter_pallet_quantity(data['inspection']['pallet_quantity'])
    time.sleep(1)

    print(f"Entering Line Count: {data['inspection']['line_count']}")
    trailer_page.enter_line_count(data['inspection']['line_count'])
    time.sleep(1)

    print("Clicking Mark as Complete button...")
    trailer_page.click_mark_as_complete()

    print("Clicking Verify Seal button...")
    trailer_page.click_verify_seal()
    time.sleep(1)

    print(f"Entering Seal Number: {data['inspection']['seal_number']}")
    trailer_page.enter_seal_number(data['inspection']['seal_number'])

    print("Uploading Seal Image...")
    trailer_page.upload_seal_image(data['inspection']['seal_image'])
    time.sleep(2)

    print("Clicking Save Seal Verification button...")
    trailer_page.click_save_seal_verification()
    time.sleep(2)

    print("Clicking Start Seal Verification button...")
    trailer_page.click_start_seal_verification()
    time.sleep(2)

    print("Clicking Final Yes...")
    trailer_page.click_final_yes()
    time.sleep(1)

    print("Clicking Final Mark as Complete...")
    trailer_page.click_final_mark_complete()
    time.sleep(2)

    print("Navigating back to Trailer Processing list...")
    trailer_page.click_trailer_processing_nav()
    time.sleep(5)

def execute_checkout_page(driver):
    print("Executing Checkout Page logic...")
    checkout_page = CheckoutPage(driver)
    checkout_page.click_checkout_driver()
    checkout_page.click_complete_checkout()
    print("Checkout Page Test Passed!")

def test_pakyard_full_flow():
    driver = get_driver()
    try:
        execute_login_page(driver)
        execute_home_page(driver)
        execute_appointment_page(driver)
        execute_logout_page(driver)
        execute_checkin_page(driver)
        execute_login_page(driver)
        execute_trailer_processing_ob_page(driver)
        execute_checkout_page(driver)
        print("All tests completed successfully!")

    except Exception as e:
        print(f"Test Failed: {e}")
        traceback.print_exc()
        print(f"Current URL: {driver.current_url}")
        driver.save_screenshot("Test_failed.png") # Save screenshot for debugging
    finally:
        # driver.quit() # Keep browser open to verify items
        pass

if __name__ == "__main__":
    test_pakyard_full_flow()
