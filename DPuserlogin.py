from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_pakyard_login():
    options = webdriver.ChromeOptions()
    # Use a user data directory to persist login session
    options.add_argument("user-data-dir=C:\\Users\\Admin\\Python\\PAKYARD\\ChromeData")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://dev.pakyard.drinkpak.com/login")
        driver.maximize_window()
        wait = WebDriverWait(driver, 20)

        # If redirected to home/dashboard due to saved session, logout to show login page
        if "/home" in driver.current_url or "dashboard" in driver.current_url:
            driver.delete_all_cookies()
            driver.get("https://dev.pakyard.drinkpak.com/login")

        sso_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'SSO Login with Microsoft')] | //a[contains(., 'SSO Login with Microsoft')]")))
        sso_button.click()
            
        # Assert that login was successful (e.g., by checking for an element on the dashboard)
        # Example: Check for a common element on the dashboard after successful login
        dashboard_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(., 'Welcome to the PAKYARD')] | //h1[contains(., 'Dashboard')]")))
        assert dashboard_element.is_displayed()
        print("Login successful!")

        # Wait for Bulletin Board items to load
        print("Waiting for Bulletin Board items to appear...")
        time.sleep(5)

    except Exception as e:
        print(f"Login failed: {e}")
        print(f"Current URL: {driver.current_url}")
        driver.save_screenshot("login_failed.png") # Save screenshot for debugging
    finally:
        # driver.quit() # Keep browser open to verify items
        pass

if __name__ == "__main__":
    test_pakyard_login()
