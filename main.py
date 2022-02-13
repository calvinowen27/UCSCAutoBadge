from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from twilio.rest import Client
import datetime
import requests

URL = 'https://studenthealth.ucsc.edu/'

info = open('info.txt').read().split()

# User info
USER = info[0]
PASS = info[1]
MONTH = info[2]
DAY = info[3]
YEAR = info[4]

# twilio info
twilio_account_sid = info[5]
twilio_auth_token = info[6]

client = Client(twilio_account_sid, twilio_auth_token)

driver = webdriver.Chrome()
driver.get(URL)


def login():
    # Type username
    user_field = driver.find_element(By.ID, 'username')
    user_field.click()
    pyautogui.write(USER)

    # Type password
    user_field = driver.find_element(By.ID, 'password')
    user_field.click()
    pyautogui.write(PASS)

    # Login
    pyautogui.hotkey('return')


def verify_birthday():
    # Set month
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dtDOBMN"))).click()
    pyautogui.write(MONTH)

    # Set day
    driver.find_element(By.ID, 'dtDOBDY').click()
    pyautogui.write(DAY)

    # Set Year
    driver.find_element(By.ID, 'dtDOBYR').click()
    pyautogui.write(YEAR)

    # Proceed
    driver.find_element(By.ID, 'cmdStandardProceed').click()


def do_survey():
    # Navigate to survey
    # Complete Survey Button
    driver.find_element(By.LINK_TEXT, 'Complete Survey').click()

    # Continue Button
    driver.find_element(By.LINK_TEXT, 'Continue').click()

    # Answer survey questions
    driver.find_element(By.XPATH, '//*[@id="mainbody"]/main/form/div[2]/fieldset/div[2]').click()
    driver.find_element(By.XPATH, '//*[@id="mainbody"]/main/form/div[3]/fieldset/div/div[2]/div').click()
    driver.find_element(By.XPATH, '//*[@id="mainbody"]/main/form/div[4]/fieldset/div/div[2]/div').click()
    driver.find_element(By.XPATH, '//*[@id="mainbody"]/main/form/div[5]/fieldset/div/div[2]/div').click()
    driver.find_element(By.XPATH, '//*[@id="mainbody"]/main/form/div[6]/fieldset/div/div[2]/div').click()
    driver.find_element(By.XPATH, '//*[@id="mainbody"]/main/form/div[7]/fieldset/div[1]').click()

    # Continue Button
    driver.find_element(By.XPATH, '//*[@id="mainbody"]/header/div/div[2]/input').click()

    # Show Badge Button
    driver.find_element(By.XPATH, '//*[@id="showQuarantineBadge"]').click()


def screenshot():
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="quarantineBadge"]/h1')))
    ss = pyautogui.screenshot()
    path = f'{datetime.datetime.now().date()}.png'
    ss.save(path)
    return path


def upload_image(path):
    file = open(path)
    r = requests.post('https://localhost/', files=file)
    print(r.text)


def send_message():
    client.messages.create(
        body='Hi there',
        from_='+14253074616',
        to='+14259855538'
    )


def main():
    login()
    verify_birthday()
    do_survey()
    upload_image(screenshot())
    #send_message()


if __name__ == '__main__':
    main()
