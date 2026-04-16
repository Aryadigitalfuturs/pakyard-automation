from selenium import webdriver
import json
import traceback
import time
from datetime import datetime
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
from manualcheckinpage import ManualCheckInPage
from ReportManager import ReportManager

def get_driver():
    options = webdriver.ChromeOptions()
    # Use a user data directory to persist login session
    options.add_argument("user-data-dir=C:\\Users\\Admin\\Python\\PAKYARD\\ChromeData")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream_camera": 1})
    driver = webdriver.Chrome(options=options)
    return driver

def execute_login_page(driver, report):
    login_page = LoginPage(driver)
    report.log_step("Navigation", "INFO", "Navigating to Login Page")
    try:
        login_page.load()
    except Exception as e:
        if "net::ERR_NAME_NOT_RESOLVED" in str(e):
            report.log_step("DNS Check", "FAIL", "DNS Resolution Failed. VPN might be disconnected.")
            print("The domain 'dev.pakyard.drinkpak.com' could not be reached.")
            print("Please ensure you are connected to the VPN or check your internet connection.\n")
        raise e

    driver.maximize_window()

    # If redirected to home/dashboard due to a saved session, we are already logged in.
    if "/home" in driver.current_url or "dashboard" in driver.current_url:
        report.log_step("Authentication", "PASS", "Already logged in via session data.")
        return

    report.log_step("Authentication", "INFO", "Attempting SSO Login.")
    login_page.click_sso()

    # Check if we are redirected to the Microsoft Login (which asks for Username/Password)
    if "login.microsoftonline.com" in driver.current_url:
        report.log_step("SSO Manual Interaction", "INFO", "Redirected to Microsoft. Manual intervention may be required.")

    # Wait for the URL to change, confirming login was successful
    WebDriverWait(driver, 30).until(lambda d: "/home" in d.current_url or "dashboard" in d.current_url)
    report.log_step("Login Page", "PASS", "Dashboard reached successfully.")

def execute_home_page(driver, report):
    # Check for login or expired session URL
    if "login" in driver.current_url or "session=expired" in driver.current_url:
        report.log_step("Session Management", "INFO", "Session expired. Re-authenticating...")
        execute_login_page(driver, report)
    
    # Explicitly wait for the dashboard/home URL to ensure login finished
    try:
        WebDriverWait(driver, 20).until(
            lambda d: "/home" in d.current_url or "dashboard" in d.current_url
        )
        report.log_step("Home Page Load", "PASS", "Currently on dashboard.")
    except TimeoutException:
        error_img = "err_dashboard.png"
        driver.save_screenshot(error_img)
        report.log_step("Home Page Load", "FAIL", f"Timed out waiting for dashboard. URL: {driver.current_url}", error_img)
        raise

    home_page = HomePage(driver)
    # Using explicit wait and the provided XPath for robustness
    appointment_link_xpath = "//a[contains(@href, '/appointment')] | //a[contains(., 'Appointment')] | /html/body/div[2]/div[1]/div[2]/a[3]"
    appointment_link = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, appointment_link_xpath))
    )
    appointment_link.click()
    print("Home Page Test Passed!")

def execute_appointment_page(driver, report):
    appointment_page = AppointmentObPage(driver)
    
    # Verify Appointment page loaded
    if appointment_page.is_loaded():
        report.log_step("Appointment Page", "PASS", "Appointment Schedule page loaded successfully!")

    # Click on the Outbound button to view outbound appointments
    report.log_step("Appointment Filters", "INFO", "Clicking 'Outbound' button on appointment page...")
    outbound_button_xpath = "/html/body/div[2]/div[2]/div/div/div/div[3]/div[1]/div/div[1]/div/button[2]"
    # The click was being intercepted by a loading overlay, causing an ElementClickInterceptedException.
    # We will wait for the button to be present and then use a JavaScript click to bypass the overlay.
    outbound_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, outbound_button_xpath))
    )
    driver.execute_script("arguments[0].click();", outbound_button)
    time.sleep(3) # Wait for the appointment list to refresh

    # with open(r"c:\Users\Admin\Python\PAKYARD\test_data.json", "r") as f:
    #     data = json.load(f)

    # for appointment in data["appointments"]:
    #     print(f"Selecting customer: {appointment['customer']}")
    #     appointment_page.select_customer(appointment['customer'])
    #     time.sleep(5)
    #     print(f"Clicking + icon for time: {appointment['time']}")
    #     appointment_page.select_time_slot(appointment['time'])
    #     time.sleep(5)
        
    #     if "carrier" in appointment:
    #         print(f"Selecting carrier: {appointment['carrier']}")
    #         appointment_page.select_carrier(appointment['carrier'])
    #         time.sleep(2)

    #     if "shipment_id" in appointment:
    #         print(f"Entering Shipment ID: {appointment['shipment_id']}")
    #         appointment_page.enter_shipment_id(appointment['shipment_id'])
    #         time.sleep(2)

    #     if "order_type" in appointment:
    #         print(f"Selecting Order Type: {appointment['order_type']}")
    #         appointment_page.select_order_type(appointment['order_type'])
    #         time.sleep(2)

    #     if "contact_name" in appointment:
    #         print(f"Entering Contact Name: {appointment['contact_name']}")
    #         appointment_page.enter_contact_name(appointment['contact_name'])
    #         time.sleep(2)

    #     if "contact_number" in appointment:
    #         print(f"Entering Contact Number: {appointment['contact_number']}")
    #         appointment_page.enter_contact_number(appointment['contact_number'])
    #         time.sleep(2)

    #     if "email" in appointment:
    #         print(f"Entering Email: {appointment['email']}")
    #         appointment_page.enter_email(appointment['email'])
    #         time.sleep(2)

    #     print("Clicking Save button...")
    #     appointment_page.click_save()
    #     time.sleep(5) # Removed as per previous instruction to skip BOL
    report.log_step("Appointment Page", "PASS", "Outbound appointments displayed.")

def execute_manual_checkin(driver, report):
    report.log_step("Manual Check-in", "INFO", "Executing Manual Check-in...")
    manual_checkin_page = ManualCheckInPage(driver)
    
    with open(r"c:\Users\Admin\Python\PAKYARD\test_data.json", "r") as f:
        data = json.load(f)

    shipment_id = data['appointments'][0]['shipment_id']

    try:
        manual_checkin_page.click_trailer_icon(shipment_id)
        manual_checkin_page.enter_driver_name(data['checkin']['driver_name'])
        manual_checkin_page.enter_trailer_number(data['checkin']['trailer_number'])
        manual_checkin_page.select_trailer_type(data['checkin']['trailer_type'])
        time.sleep(2)  # Allow UI to stabilize after trailer type selection
        
        # Select Carrier then Select Comment
        manual_checkin_page.select_carrier(data['checkin']['carrier'])
        if 'ontime_comment' in data['checkin']:
            manual_checkin_page.select_ontime_comment(data['checkin']['ontime_comment'])

        manual_checkin_page.click_confirm_checkin()

        if 'dock_door' in data:
            manual_checkin_page.select_dock_door(data['dock_door'])
            manual_checkin_page.click_assign_dock_door()

        manual_checkin_page.click_done()
    except Exception as e:
        error_img = f"err_checkin_{shipment_id}.png"
        driver.save_screenshot(error_img)
        report.log_step("Check-in", "FAIL", f"Failed during Manual Check-in: {e}", error_img)
        raise

# def execute_logout_page(driver):
#     logout_page = LogoutPage(driver)
#     print("Clicking Logout button...")
#     logout_page.click_logout()
#     time.sleep(2)
#     print("Confirming Logout...")
#     logout_page.click_confirm_logout()
#     time.sleep(3)
#     print("Logout Page Test Passed!")

# def execute_checkin_page(driver):
#     checkin_page = CheckInPage(driver)
#     print("Navigating to Check-In Page...")
#     checkin_page.load()
#     time.sleep(2)
#     code = input("Enter Confirmation Number : ")
#     checkin_page.enter_code(code)
#     checkin_page.click_confirm()
#     time.sleep(2)

#     with open(r"c:\Users\Admin\Python\PAKYARD\test_data.json", "r") as f:
#         data = json.load(f)
#     checkin_page.enter_driver_name(data["checkin"]["driver_name"])
#     checkin_page.enter_driver_cell(data["checkin"]["driver_cell"])
#     checkin_page.enter_license_number(data["checkin"]["license_number"])
#     checkin_page.select_license_state(data["checkin"]["license_state"])
#     checkin_page.enter_tractor_number(data["checkin"]["tractor_number"])
#     checkin_page.select_trailer_type(data["checkin"]["trailer_type"])
#     checkin_page.enter_trailer_number(data["checkin"]["trailer_number"])
#     checkin_page.upload_document(data["checkin"]["document_path"])
#     checkin_page.click_finish()
#     time.sleep(5)
#     print("Check-In Page Test Passed!")

def execute_trailer_processing_ob_page(driver, report):
    home_page = HomePage(driver)
    # The is_dashboard_displayed check can cause a TimeoutException if the current page isn't the dashboard.
    # if home_page.is_dashboard_displayed():
    #     print("Dashboard displayed.")
    report.log_step("Navigation", "INFO", "Navigating to Trailer Processing screen...")
    home_page.click_trailer_processing()
    trailer_page = TrailerProcessingObPage(driver)
    if trailer_page.is_loaded():
        report.log_step("Trailer Processing", "PASS", "Trailer Processing page loaded successfully!")
    
    with open(r"c:\Users\Admin\Python\PAKYARD\test_data.json", "r") as f:
        data = json.load(f)

    report.log_step("Trailer Processing", "INFO", "Clicking View button...")
    trailer_page.click_view_button()
    time.sleep(2)

    report.log_step("Inspection", "INFO", "Clicking Start Inspection button...")
    trailer_page.click_start_inspection()
    time.sleep(2)

    report.log_step("Inspection", "INFO", f"Entering Inspector Name: {data['inspection']['inspector_name']}")
    trailer_page.enter_inspector_name(data['inspection']['inspector_name'])
    trailer_page.click_yes_for_all_questions()
    trailer_page.check_and_upload_photo(data['checkin']['document_path'])
    report.log_step("Inspection", "INFO", "Clicking Save Inspection button...")
    trailer_page.click_save_inspection() # This was missing a log_step
    report.log_step("Inspection", "PASS", "Trailer inspection completed.")
    time.sleep(5)

    report.log_step("Loading", "INFO", "Clicking Start Loading button...")
    trailer_page.click_start_loading() # This was missing a log_step
    report.log_step("Loading", "INFO", f"Entering Loader Name: {data['inspection']['loader_name']}")
    trailer_page.enter_loader_name(data['inspection']['loader_name']) # This was missing a log_step
    report.log_step("Loading", "INFO", f"Entering Pallet Quantity: {data['inspection']['pallet_quantity']}")
    trailer_page.enter_pallet_quantity(data['inspection']['pallet_quantity']) # This was missing a log_step
    report.log_step("Loading", "INFO", f"Entering Line Count: {data['inspection']['line_count']}")
    trailer_page.enter_line_count(data['inspection']['line_count']) # This was missing a log_step
    report.log_step("Loading", "INFO", "Clicking Mark as Complete button...")
    trailer_page.click_mark_as_complete() # This was missing a log_step
    report.log_step("Loading", "PASS", "Loading details submitted.")

    report.log_step("Seal Verification", "INFO", "Clicking Verify Seal button...")
    trailer_page.click_verify_seal() # This was missing a log_step
    report.log_step("Seal Verification", "INFO", f"Entering Seal Number: {data['inspection']['seal_number']}")
    trailer_page.enter_seal_number(data['inspection']['seal_number']) # This was missing a log_step
    report.log_step("Seal Verification", "INFO", "Uploading Seal Image...")
    trailer_page.upload_seal_image(data['inspection']['seal_image']) # This was missing a log_step
    report.log_step("Seal Verification", "INFO", "Clicking Save Seal Verification button...")
    trailer_page.click_save_seal_verification() # This was missing a log_step
    report.log_step("Seal Verification", "INFO", "Clicking Start Seal Verification button...")
    trailer_page.click_start_seal_verification() # This was missing a log_step
    report.log_step("Seal Verification", "INFO", "Clicking Final Yes...")
    trailer_page.click_final_yes() # This was missing a log_step
    report.log_step("Seal Verification", "INFO", "Clicking Final Mark as Complete...")
    trailer_page.click_final_mark_complete() # This was missing a log_step
    report.log_step("Seal Verification", "PASS", "Seal verified and marked complete.")

    report.log_step("Checkout", "INFO", "Clicking Complete Check Out Complete button...")
    trailer_page.click_complete_checkout_main() # This was missing a log_step
    report.log_step("Checkout", "INFO", "Clicking Continue button...")
    trailer_page.click_continue_modal_button() # This was missing a log_step
    report.log_step("Checkout", "PASS", "Checkout process finalized.")

def execute_checkout_page(driver, report):
    report.log_step("Checkout", "INFO", "Executing Checkout flow on the Trailer Processing detail page...")
    trailer_page = TrailerProcessingObPage(driver)
    
    trailer_page.click_go_to_checkout()
    time.sleep(2)
    trailer_page.click_start_checkout_final()
    time.sleep(2)
    trailer_page.click_complete_checkout_final()
    report.log_step("Checkout Page", "PASS", "Checkout process completed from detail page.")

def test_pakyard_full_flow():
    report = ReportManager()
    driver = None
    try:
        driver = get_driver()
        execute_login_page(driver, report)
        execute_home_page(driver, report)
        execute_appointment_page(driver, report)
        execute_manual_checkin(driver, report)
        execute_trailer_processing_ob_page(driver, report)
        
        report.log_step("Final Status", "PASS", "All workflow segments finished successfully.")

    except Exception as e:
        screenshot = f"Final_Failure_{datetime.now().strftime('%H%M%S')}.png"
        if driver:
            driver.save_screenshot(screenshot)
        report.log_step("CRITICAL FAILURE", "FAIL", str(e), screenshot)
        traceback.print_exc()
    finally:
        if driver:
            # driver.quit()
            pass
        report.generate_report()

if __name__ == "__main__":
    test_pakyard_full_flow()
