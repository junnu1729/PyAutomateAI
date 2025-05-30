import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging at the very top
logging.basicConfig(
    filename='rpa_log.log',  # Log file name
    level=logging.INFO,      # Log level (INFO or DEBUG for more detail)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load config
with open("config.json") as f:
    config = json.load(f)

username = config["username"]
password = config["password"]
login_url = config["login_url"]

# Setup Chrome options
options = Options()
# options.headless = True  # Uncomment to run headless (no browser window)

# Setup Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    logging.info(f"Opening login page: {login_url}")
    driver.get(login_url)
    time.sleep(1)

    logging.info("Filling login form...")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    time.sleep(2)  # Wait for page to load after login

    # Verify login success by checking for an element with id="dashboard"
    try:
        driver.find_element(By.ID, "dashboard")  # Adjust if your dashboard uses a different ID
        logging.info("Login successful! Dashboard found.")
    except NoSuchElementException:
        logging.warning("Login failed or dashboard element not found.")

except Exception as e:
    logging.exception(f"An error occurred: {e}")

finally:
    logging.info("Closing browser...")
    driver.quit()
