"""
This script automates the process of opening a URL in Chrome, opening the Developer Tools, and performing a search within the Developer Tools.

Requirements:
- Selenium: `pip install selenium`
- WebDriver Manager: `pip install webdriver_manager`
- PyAutoGUI: `pip install pyautogui`

Usage:
1. Run the script from the command line.
2. Enter the URL you want to open.
3. Enter the value you want to search for in the Developer Tools.

Note: It is recommended to run this script with administrator privileges to ensure all actions are performed correctly.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import time

# Prompt for URL and search value
url = input("Enter the URL: ")
search_value = input("Enter the value to search: ")

# Set up Chrome options to auto-open Developer Tools and exclude logging
chrome_options = Options()
chrome_options.add_argument("--auto-open-devtools-for-tabs")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Set up the WebDriver using webdriver_manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL
driver.get(url)

# Wait for Developer Tools to open
time.sleep(2)

# Use pyautogui to open the search in Developer Tools (Ctrl + F)
pyautogui.hotkey('ctrl', 'f')

# Wait for the search box to appear
time.sleep(1)

# Enter the search value
pyautogui.typewrite(search_value)

# Wait for a bit to see the results
time.sleep(5)

# Prevent the browser from closing
input("Press Enter to close the browser...")

# Close the browser
driver.quit()