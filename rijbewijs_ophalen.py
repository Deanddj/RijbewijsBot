import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import platform
from dotenv import load_dotenv

script_directory = os.path.dirname(os.path.realpath(__file__))
if platform.system() == "Windows":
    chrome_driver_path = os.path.join(script_directory, "chromedriver.exe")
else:
    chrome_driver_path = os.path.join(script_directory, "chromedriver")

load_dotenv()
ophaal_url = os.getenv('OPHAAL_WEBHOOK_URL')

service = Service(chrome_driver_path)

# Voeg eventueel extra opties toe
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=RijbewijsNotifier/1.0 (+https://github.com/Deanddj/RijbewijsBot)')

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://zoetermeer.qmatic.io/booking/singlebooking?selectedService=a4529ff9-ce0a-4fcb-bfc3-781910725bf6&selectedBranch=06f5e18f-c62d-4134-89ba-a7a83cf454d7")

    wait = WebDriverWait(driver, 10)

    date_container = wait.until(EC.visibility_of_element_located((
        By.XPATH,
        '/html/body/div/div/div/div/div[1]/main/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]'
    )))

    p_elements = date_container.find_elements(By.TAG_NAME, 'p')

    data = (p_elements[0].text, p_elements[1].text, p_elements[2].text)

    print(f"Het eerstvolgende ophaalmoment is {data[1]} ({data[0]}), {data[2]}")

    file_path = os.path.join(script_directory, "extracted_data_ophaal.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            previous_data = file.read().strip()

        if data[0] != previous_data:
            with open(file_path, "w") as file:
                file.write(data[0])

            discord_webhook_url = str(ophaal_url)
            payload = {"content": f"Het eerstvolgende ophaalmoment is {data[1]} ({data[0]}), {data[2]}"}
            requests.post(discord_webhook_url, json=payload)
    else:
        with open(file_path, "w") as file:
            file.write(data[0])

        discord_webhook_url = str(ophaal_url)
        payload = {"content": f"Het eerstvolgende ophaalmoment is {data[1]} ({data[0]}), {data[2]}"}
        requests.post(discord_webhook_url, json=payload)

finally:
    driver.quit()
    print(f"Script voltooid om: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")