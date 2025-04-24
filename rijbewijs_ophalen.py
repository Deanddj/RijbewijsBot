import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import platform
from dotenv import load_dotenv

script_directory = os.path.dirname(os.path.realpath(__file__))
if platform.system() == "Windows":
    chrome_driver_path = os.path.join(script_directory, "chromedriver.exe")
else:
    chrome_driver_path = os.path.join(script_directory, "chromedriver")

load_dotenv()
ophaal_url = os.getenv('OPHAAL_WEBHOOK_URL')
aantal_dagen = int(os.getenv('BINNEN_AANTAL_DAGEN'))

current_date_obj = datetime.today()
max_allowed_date = current_date_obj + timedelta(days=aantal_dagen)

service = Service(chrome_driver_path)

# Chrome driver setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=RijbewijsNotifier/1.0 (+https://github.com/Deanddj/RijbewijsBot)')

def notify(content):
    requests.post(ophaal_url, json={"content": content})

file_path = os.path.join(script_directory, "extracted_data_ophaal.txt")

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
    data_date = datetime.strptime(data[0], "%d-%m-%Y")

    print(f"Het eerstvolgende ophaalmoment is {data[1]} ({data[0]}), {data[2]}")

    previous_data = None
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            previous_data = file.read().strip()

    previous_date_obj = datetime.strptime(previous_data, "%d-%m-%Y") if previous_data else None
    within_range = data_date <= max_allowed_date

    # CASE 1: Geen vorige datum en nieuwe datum is binnen bereik
    if not previous_data and within_range:
        with open(file_path, "w") as file:
            file.write(data[0])
        notify(f"Nieuw ophaalmoment gevonden: {data[1]} ({data[0]}), {data[2]}")

    # CASE 2: Vorige datum bestaat, maar is nu buiten bereik
    elif previous_date_obj and previous_date_obj > max_allowed_date:
        with open(file_path, "w") as file:
            file.truncate(0)
        notify(f"Het vorige ophaalmoment ({previous_data}) is verlopen (buiten {aantal_dagen} dagen) en is verwijderd.")

    # CASE 3: Nieuwe datum is binnen bereik en eerder dan of anders dan de vorige
    elif within_range and (not previous_date_obj or data_date < previous_date_obj or data[0] != previous_data):
        with open(file_path, "w") as file:
            file.write(data[0])
        notify(f"Beter of nieuw ophaalmoment gevonden: {data[1]} ({data[0]}), {data[2]}")

finally:
    driver.quit()
    print(f"Script voltooid om: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")