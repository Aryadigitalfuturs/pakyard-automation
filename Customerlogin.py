from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_pakyard_login():
    driver = webdriver.Chrome()  # Or any other browser driver you prefer
    try:
        driver.get("https://dev.pakyard.drinkpak.com/")
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)

        # Find username and password fields and enter credentials
        username_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='username' or @name='email' or @type='email' or @name='loginfmt']")))
        username_field.clear()
        username_field.send_keys("PAKYARD-TES-005")  # Replace with a valid username

        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password' or @name='passwd']")))
        password_field.clear()
        password_field.send_keys("Arya@123")  # Replace with a valid password

        # Click the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' or contains(., 'Login') or contains(., 'Sign in')] | //input[@type='submit']")))
        login_button.click()

        # Assert that login was successful (e.g., by checking for an element on the dashboard)
        # Example: Check for a common element on the dashboard after successful login
        dashboard_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Dashboard')]")))
        assert dashboard_element.is_displayed()
        print("Login successful!")
    except Exception as e:
        print(f"Login failed: {e}")
        driver.save_screenshot("login_failed.png") # Save screenshot for debugging
    finally:
        driver.quit()

if __name__ == "__main__":
    test_pakyard_login()
