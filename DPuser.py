from selenium import webdriver
import json
import traceback
import time
from LoginPage import LoginPage
from HomePage import HomePage
from AppointmentPage import AppointmentPage
from LogoutPage import LogoutPage
from CheckInPage import CheckInPage
from TrailerProcessingPage import TrailerProcessingPage

def get_driver():
    options = webdriver.ChromeOptions()
    # Use a user data directory to persist login session
    options.add_argument("user-data-dir=C:\\Users\\Admin\\Python\\PAKYARD\\ChromeData")
    driver = webdriver.Chrome(options=options)
    return driver

def execute_login_page(driver):
    login_page = LoginPage(driver)
    login_page.load()
    driver.maximize_window()

    # If redirected to home/dashboard due to saved session, logout to show login page
    if "/home" in driver.current_url or "dashboard" in driver.current_url:
        driver.delete_all_cookies()
        login_page.load()

    print("Clicking SSO button...")
    login_page.click_sso()
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
    appointment_page = AppointmentPage(driver)
    
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

        if "receipt_id" in appointment:
            print(f"Entering Receipt ID: {appointment['receipt_id']}")
            appointment_page.enter_receipt_id(appointment['receipt_id'])
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

def execute_trailer_processing_page(driver):
    home_page = HomePage(driver)
    if home_page.is_dashboard_displayed():
        print("Dashboard displayed.")
    print("Navigating to Trailer Processing screen...")
    home_page.click_trailer_processing()
    trailer_page = TrailerProcessingPage(driver)
    if trailer_page.is_loaded():
        print("Trailer Processing page loaded successfully!")
    
    print("Clicking View button...")
    trailer_page.click_view_button()
    time.sleep(2)

    print("Clicking Start Inspection button...")
    trailer_page.click_start_inspection()
    time.sleep(2)

    with open(r"c:\Users\Admin\Python\PAKYARD\test_data.json", "r") as f:
        data = json.load(f)

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

    print("Clicking Yes for all questions in loading page...")
    trailer_page.click_yes_for_all_questions()

    print("Checking for photo upload in loading page...")
    trailer_page.check_and_upload_photo(data['checkin']['document_path'])

    print("Clicking confirmation checkbox...")
    trailer_page.click_confirm_checkbox()
    time.sleep(2)

    print("Clicking Mark as Complete button...")
    trailer_page.click_mark_as_complete()

    print("Navigating back to Trailer Processing list...")
    trailer_page.click_trailer_processing_nav()
    time.sleep(5)

def test_pakyard_full_flow():
    driver = get_driver()
    try:
        execute_login_page(driver)
        execute_home_page(driver)
        execute_appointment_page(driver)
        execute_logout_page(driver)
        execute_checkin_page(driver)
        execute_login_page(driver)
        execute_trailer_processing_page(driver)
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
