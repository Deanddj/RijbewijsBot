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
aanvraag_url = os.getenv('AANVRAAG_WEBHOOK_URL')
aantal_dagen = int(os.getenv('BINNEN_AANTAL_DAGEN'))

current_date_obj = datetime.today()
max_allowed_date = current_date_obj + timedelta(days=aantal_dagen)

# Chrome driver setup
service = Service(chrome_driver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=RijbewijsNotifier/1.0 (+https://github.com/Deanddj/RijbewijsBot)')

def notify(msg):
    payload = {"content": msg}
    requests.post(aanvraag_url, json=payload)

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://zoetermeer.qmatic.io/booking/singlebooking?selectedService=b1528c52-78d2-4bc2-9552-768894f19256&selectedBranch=06f5e18f-c62d-4134-89ba-a7a83cf454d7")

    wait = WebDriverWait(driver, 10)
    date_container = wait.until(EC.visibility_of_element_located((
        By.XPATH,
        '/html/body/div[1]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div[1]/div/div[2]/div[2]'
    )))

    p_elements = date_container.find_elements(By.TAG_NAME, 'p')
    data = (p_elements[0].text, p_elements[1].text, p_elements[2].text)
    data_date = datetime.strptime(data[0], "%d-%m-%Y")

    print(f"Het eerstvolgende aanvraagmoment is {data[1]} ({data[0]}), {data[2]}")

    file_path = os.path.join(script_directory, "extracted_data_aanvraag.txt")
    previous_data = None
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            previous_data = file.read().strip()

    previous_date_obj = datetime.strptime(previous_data, "%d-%m-%Y") if previous_data else None
    binnen_bereik = data_date <= max_allowed_date

    # CASE 1: Geen vorige datum en nieuwe datum is binnen bereik
    if not previous_data and binnen_bereik:
        with open(file_path, "w") as file:
            file.write(data[0])
        notify(f"Nieuw aanvraagmoment gevonden: {data[1]} ({data[0]}), {data[2]}")

    # CASE 2: Vorige datum bestaat, maar is buiten bereik
    elif previous_date_obj and previous_date_obj > max_allowed_date:
        with open(file_path, "w") as file:
            file.truncate(0)
        notify(f"Het vorige aanvraagmoment ({previous_data}) is verlopen (buiten {aantal_dagen} dagen) en is verwijderd.")

    # CASE 3: Nieuwe datum is beter (eerder of anders), en binnen bereik
    elif binnen_bereik and (not previous_date_obj or data_date < previous_date_obj or data[0] != previous_data):
        with open(file_path, "w") as file:
            file.write(data[0])
        notify(f"Beter of nieuw aanvraagmoment gevonden: {data[1]} ({data[0]}), {data[2]}")

finally:
    driver.quit()
    print(f"Script voltooid om: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")