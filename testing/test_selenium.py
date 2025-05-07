"""
Python file to test the web application using Selenium, with element highlighting.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time

def start_browser():
    """Start the browser with WebDriver Manager and open up the page."""
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('http://127.0.0.1:5000')
    driver.maximize_window()  # Ensure the window is maximized
    print(f'Page Title: {driver.title}')
    time.sleep(3)
    return driver

def highlight(driver, element):
    """Highlights (blinks) a Selenium WebDriver element."""
    driver.execute_script("arguments[0].style.border='3px solid lime'", element)


def click_element(driver, element):
    """Highlight and click an element."""
    highlight(driver, element)
    ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(0.5)

def register(driver, first_name, email, nuid, password):
    wait = WebDriverWait(driver, 5)

    try:
        uno_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Email")))
        click_element(driver, uno_button)
        print("Clicked Email button.")

        register_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Not a member? Register here")))
        click_element(driver, register_button)
        print("Clicked Register button.")

        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])

        fields = {
            "first_name": first_name,
            "email": email,
            "nuid": nuid,
            "password": password,
            "confirm_password": password
        }

        for field_id, value in fields.items():
            field = driver.find_element(By.ID, field_id)
            highlight(driver, field)
            field.send_keys(str(value))
            time.sleep(0.3)

        print("Filled registration form.")

        submit_button = driver.find_element(By.XPATH, "//button[text()='Register']")
        click_element(driver, submit_button)
        print("Submitted registration form.")

    except Exception as e:
        print(f"Registration failed: {e}")

def login_email(driver, email, password):
    wait = WebDriverWait(driver, 10)

    try:
        uno_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Email")))
        click_element(driver, uno_button)
        print("Clicked Email button.")

        time.sleep(1)

        identifier_field = driver.find_element(By.ID, "identifier")
        highlight(driver, identifier_field)
        identifier_field.send_keys(email)
        time.sleep(0.5)

        password_field = driver.find_element(By.ID, "password")
        highlight(driver, password_field)
        password_field.send_keys(password)
        time.sleep(0.5)

        print("Filled email sign in.")

        login_button = driver.find_element(By.XPATH, "//button[text()='Login']")
        click_element(driver, login_button)
        print("Clicked Login button.")

        time.sleep(3)

    except Exception as e:
        print(f"Login with email failed: {e}")

def back_to_signin(driver):
    try:
        time.sleep(1)
        driver.back()
        print("Went back one page.")

        back_link = driver.find_element(By.LINK_TEXT, "Back to Login Selection")
        click_element(driver, back_link)
        print("Clicked back to sign in selection button.")

        time.sleep(1)

    except Exception as e:
        print(f"Going back failed: {e}")

def login_nuid(driver, nuid, password):
    wait = WebDriverWait(driver, 10)

    try:
        driver.switch_to.window(driver.window_handles[-1])

        print(f"Current URL: {driver.current_url}")

        nuid_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "NUID")))
        click_element(driver, nuid_button)
        print("Clicked NUID button.")

        time.sleep(1)

        identifier_field = driver.find_element(By.ID, "identifier")
        highlight(driver, identifier_field)
        identifier_field.send_keys(str(nuid))
        time.sleep(0.5)

        password_field = driver.find_element(By.ID, "password")
        highlight(driver, password_field)
        password_field.send_keys(password)
        time.sleep(0.5)

        print("Filled NUID sign in.")

        login_button = driver.find_element(By.XPATH, "//button[text()='Login']")
        click_element(driver, login_button)
        print("Clicked Login button.")

        time.sleep(3)

    except Exception as e:
        print(f"Login with NUID failed: {e}")

def run_predictions(driver):
    try:
        # Clear the field and input the new value
        class_code_field = driver.find_element(By.ID, "class_code")
        highlight(driver, class_code_field)
        class_code_field.clear()  # Clear any existing text
        class_code_field.send_keys("CSCI3320")
        time.sleep(1)

        # Find the dropdown element
        dropdown_element = driver.find_element(By.ID, "semester")  # Get the WebElement
        highlight(driver, dropdown_element)  # Highlight the dropdown
        dropdown = Select(dropdown_element)  # Create a Select object for interacting
        dropdown.select_by_visible_text("Fall")
        time.sleep(1)

        # Find the submit button using its type attribute
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        highlight(driver, submit_button)
        submit_button.click()
        time.sleep(3)

        # Now go back to clear the form and select new values
        driver.back()
        print("Went back one page.")

        # Wait until the form is available again
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "class_code")))

        # Clear the field and input the new value
        class_code_field = driver.find_element(By.ID, "class_code")
        highlight(driver, class_code_field)
        class_code_field.clear()  # Clear any existing text
        class_code_field.send_keys("CSCI1620")
        time.sleep(1)

        # Select the new semester option
        dropdown_element = driver.find_element(By.ID, "semester")  # Get the WebElement again
        highlight(driver, dropdown_element)  # Highlight the dropdown
        dropdown = Select(dropdown_element)  # Create a new Select object for interaction
        dropdown.select_by_visible_text("Spring")
        time.sleep(1)

        # Find the submit button using its type attribute
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        highlight(driver, submit_button)
        submit_button.click()
        time.sleep(3)

    except Exception as e:
        print(f"Finding class predictions failed: {e}")


if __name__ == "__main__":
    first_name = "test-person"
    email = "test@unomaha.edu"
    nuid = 12345
    password = "test-password"

    driver = start_browser()

    register(driver, first_name, email, nuid, password)
    login_email(driver, email, password)
    back_to_signin(driver)
    login_nuid(driver, nuid, password)
    run_predictions(driver)

    driver.quit()

