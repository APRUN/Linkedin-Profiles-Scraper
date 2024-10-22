import time
import re
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import keyboard

# Automatically install the correct chromedriver
chromedriver_autoinstaller.install()

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")

# Path to chromedriver
service = Service(executable_path=chromedriver_autoinstaller.install())

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to read the first 10 rows from a text file and remove numbers and asterisks
def read_and_clean_first_10_rows(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        cleaned_lines = [re.sub(r'[\d*]', '', line).strip() for line in lines[:10]]
        return cleaned_lines, lines[10:]

# File path to the text file
file_path = 'data.txt'
csv_file_path = 'linkedin_profiles.csv'

# Check if the CSV file exists and write the header if it doesn't
if not os.path.isfile(csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'City', 'LinkedIn URL'])

# Store the handle of the original tab
original_tab = driver.current_window_handle

while True:
    # Read and clean the first 10 rows from the file
    cleaned_rows, remaining_lines = read_and_clean_first_10_rows(file_path)
    
    if not cleaned_rows:
        break

    # Loop through each row, append "Linkedin", and open in a new tab
    for row in cleaned_rows:
        search_query = row + " Linkedin"
        url = f"https://www.google.com/search?q={search_query}"

        # Open a new tab and switch to it
        driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(1)  # Wait a second to allow the tab to load
        
        # Switch to the newly opened tab
        new_tab = [handle for handle in driver.window_handles if handle != original_tab][-1]
        driver.switch_to.window(new_tab)
        
        try:
            # Click on the first Google search result
            first_result = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'h3'))
            )
            first_result.click()
            time.sleep(2)  # Wait for the LinkedIn profile to load
            
            # Print the LinkedIn URL
            print(f"Opened LinkedIn profile for: {row}")
        
        except Exception as e:
            # Print the name if LinkedIn profile is not found
            print(f"LinkedIn profile not found for: {row}")
        
        # Close the new tab after processing
        driver.close()
        # Switch back to the original tab
        driver.switch_to.window(original_tab)

    # Remove the processed lines from the file
    with open(file_path, 'w') as file:
        file.writelines(remaining_lines)

out = True
while out:
    print("open")
    if keyboard.is_pressed('esc'):
        out = False
        break
    time.sleep(1)

driver.quit()

# Keep the browser open
print("All tabs opened. You can close the browser manually.")
