from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from email.message import EmailMessage
import ssl #for security
import smtplib
import requests

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_experimental_option("detach", True)         #leaves the browser open after completing a request (it closes by default)
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

driver.get("https://my.uscis.gov/appointmentscheduler-appointment/ca/en/office-search") #
driver.maximize_window()

zip = driver.find_element(By.ID, "zip-input")
zip.send_keys("98168") #98168seattle #99102spokane
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "field_office_query"))).click()

driver.implicitly_wait(5)

try: 
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "available-appts"))).click()

    driver.implicitly_wait(5)

    element =  driver.find_element(By. CLASS_NAME, "time-text").get_attribute("innerHTML")
    result =  "Appointment available at " + element.split("for ")[1] + "."

except:
    element = driver.find_element(By.ID, "no-available-appts").get_attribute("innerHTML")
    result = "nothing yet"
    print("error in finding appt status")

if "Appointment" in result:
    email_sender = "theflashvszoom28@gmail.com"
    email_password = "slwa zrji mgsz rpzm"
    email_receiver = "najaf.ahmed@bellevuecollege.edu" #najaf.ahmed@bellevuecollege.edu

    subject = "Biometrics Appointment"
    body = result
    em = EmailMessage()
    em["Form"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

else:
    print("nothing yet")
