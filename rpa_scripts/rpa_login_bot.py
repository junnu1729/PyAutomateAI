from selenium import webdriver
import time
import pyautogui

def rpa_task():
    driver = webdriver.Chrome()
    driver.get("https://formy-project.herokuapp.com/form")
    time.sleep(5)
    print("page title:",driver.title)
    driver.quit()
    pyautogui.alert("RPA Task Completed")
rpa_task()