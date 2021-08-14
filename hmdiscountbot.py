from guerrillamail import GuerrillaMailSession
import requests
import time
import os
from datetime import date
from random import randrange
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from flask import Flask, render_template


class hm_script(object):

    def __init__(self):
        self.EMAIL_ADDRESS = ""
        self.PASSWORD = ""
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("window-size=1920x1080")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-extensions")
        # Sometimes will get blank screen aka invalid SSL certificate
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--allow-running-insecure-content')
        # Proxy
        self.chrome_options.add_argument("--proxy-server='direct://'")
        self.chrome_options.add_argument("--proxy-bypass-list=*")
        # Setting in case website blocks headless browser mode
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.chrome_options.add_argument(f'user-agent={user_agent}')
        # Give browser option to incognito
        self.chrome_options.add_argument("--incognito")
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=self.chrome_options)
        # self.driver = webdriver.Chrome(executable_path=r"C:\Users\yiyan\Downloads\chromedriver.exe", options=self.chrome_options)

    def generate_new_acc(self):
        session = GuerrillaMailSession()
        self.EMAIL_ADDRESS = session.get_session_state()['email_address']
        response = requests.get("https://www.passwordrandom.com/query?command=password")
        self.PASSWORD = response.text

        # PATH = r"C:\Users\yiyan\Downloads\chromedriver.exe"
        # driver = webdriver.Chrome(executable_path=PATH, options=chrome_options)
        driver = self.driver
        driver.implicitly_wait(2)
        # Loads the H&M website
        driver.get("https://www2.hm.com/en_us/register")

        # Debugging
        # driver.get_screenshot_as_file("screenshot1.png")

        # Accepts cookies early on to not block screen
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='onetrust-accept-btn-handler']"))).click()

        signup_page = driver.find_element_by_id("app")

        # Enters in the email address
        email_box = signup_page.find_element_by_id("email")
        email_box.send_keys(self.EMAIL_ADDRESS)

        time.sleep(1)

        # Enters in the password
        password_box = signup_page.find_element_by_name("password")
        password_box.send_keys(self.PASSWORD)

        time.sleep(1)

        # Month-Day-Year constant values
        today = date.today()
        CURR_MONTH = today.strftime("%m")
        CURR_DAY = today.strftime("%d")
        CURR_YEAR = today.strftime("%Y")
        # Make your birthday anywhere from 18  to 22 years ago
        FAKE_YEAR = str(int(CURR_YEAR) - randrange(18, 22))

        # Enters in the month for DOB
        month_box = signup_page.find_element_by_name("month")
        month_box.send_keys(CURR_MONTH)

        time.sleep(1)

        # Enters in the day for DOB
        day_box = signup_page.find_element_by_name("day")
        day_box.send_keys(CURR_DAY)

        time.sleep(1)

        # Enters in the year for DOB
        year_box = signup_page.find_element_by_name("year")
        year_box.send_keys(FAKE_YEAR)

        time.sleep(1)

        # Clicks the register button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='submitButton']"))).click()

        # driver.get_screenshot_as_file("screenshot2.png")

        print("Email Address: ", self.EMAIL_ADDRESS)
        print("Password: ", self.PASSWORD)

        time.sleep(5)

        # driver.get_screenshot_as_file("screenshot3.png")

        driver.quit()

    def get_email_address(self):
        return self.EMAIL_ADDRESS

    def get_password(self):
        return self.PASSWORD


app = Flask(__name__)


@app.route("/")
def get_account_info():
    script = hm_script()
    script.generate_new_acc()

    account_info = {
        'email': script.get_email_address(),
        'password': script.get_password()
    }
    return render_template('index.html', account_info=account_info)


if __name__ == "__main__":
    app.run()




