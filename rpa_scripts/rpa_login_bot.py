from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open your Flask login page
driver.get("http://127.0.0.1:5000/")

# Give it time to load
time.sleep(1)

# Fill in the login form (update IDs/names if needed)
driver.find_element(By.NAME, "username").send_keys("admin")
driver.find_element(By.NAME, "password").send_keys("admin123")
driver.find_element(By.XPATH, "//input[@type='submit']").click()

# Wait to see the dashboard
time.sleep(3)

# Close the browser
driver.quit()
