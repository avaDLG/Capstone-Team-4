"""
Python file to test the web application using selenium.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def start_browser():
    """Start the browser with WebDriver Manager."""
    # Create a driver instance and maximize window
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    return driver

def test_browser(driver):
    """Test the browser by opening Google and printing the page title."""
    # open page in localhose
    driver.get(' http://127.0.0.1:5000')
    
    print(f'Page Title: {driver.title}')
    
    # add some wait time to visually see the browser before it closes
    time.sleep(5)

    # Close the browser
    driver.quit()


if __name__ == "__main__":
    # Start the browser
    driver = start_browser()
    
    # Run the test
    test_browser(driver)
