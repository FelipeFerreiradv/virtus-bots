import logging
import random
import time
from task import generate_random_names, generate_random_surnames, get_phone_number, get_verification_code, fetch_emails, connect_db, save_email
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

GOOGLE_SIGNUP_URL = "https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp"
PROXY_SERVER = "Itc6tLLIatUoR93k:wifi;us;;;newland@rotating.proxyempire.io:9000"
DEFAULT_WAIT_TIME = 5000
PHONE_NUMBER_AND_ID = get_phone_number()

def random_delay(min_sec=2, max_sec=5):
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)
    return delay

def random_sex():
    set_random_sex = ["Male", "Female", "Rather not say"]
    return random.choice(set_random_sex)

class EmailAutomation:
    def __init__(self, proxy, proxy_username, proxy_password):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,
            proxy={
                "server": proxy,
                "username": proxy_username,
                "password": proxy_password
            } if proxy else None
        )

        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            viewport={"width": random.randint(1024, 1820), "height": random.randint(768, 1080)},
            locale="en-US",
            timezone_id="America/New_York"
        )
        self.page = self.context.new_page()
        logging.info("Browser opened")

    def simulate_typing(self, locator, text, delay_min=0.1, delay_max=0.3):
        """Função para simular a digitação humana de forma mais realista."""
        locator.clear()
        for char in text:
            locator.type(char)
            time.sleep(random.uniform(delay_min, delay_max))

    def create_email_account(self, email, gmail, password):
        try:
            # abrir página de signup do Google
            self.page.goto(GOOGLE_SIGNUP_URL)

            first_name = generate_random_names()
            last_name = generate_random_surnames()
            next_button = self.page.get_by_role('button')
            next_button_text = self.page.get_by_text("Next")

            try:
                if not self.page.locator('input#day').is_visible():
                    self.page.locator('input#firstName').clear()
                    self.page.fill('input#firstName', first_name)
                    self.page.locator('input#lastName').clear()
                    self.page.fill('input#lastName', last_name)
                    logging.info(f"Filled: {first_name} {last_name}")
                    next_button.click()

                self.page.wait_for_selector('input#day', timeout=DEFAULT_WAIT_TIME)
                self.page.locator('input#day').clear()
                self.page.fill('input#day', str(random.randint(1, 30)))
                self.page.get_by_label('Month').select_option("January")
                self.page.locator('input#year').clear()
                self.page.fill("input#year", str(random.randint(1940, 2000)))
                gender_select = self.page.locator("select[id = 'gender']")
                gender_select.select_option(label=f"{random_sex()}")
                next_button.click()

                time.sleep(2)
                if self.page.locator("id=selectionc4").is_visible():
                    select_radio_email = self.page.locator("id=selectionc4")
                    select_radio_email.click()

                self.page.wait_for_selector("input[name='Username']", timeout=DEFAULT_WAIT_TIME)
                self.page.locator("input[name='Username']").fill(gmail)
                logging.info("Input gmail filled")
                next_button_text.click()

                self.page.wait_for_selector("input[name='Passwd']", timeout=DEFAULT_WAIT_TIME)
                self.page.locator("input[name='Passwd']").fill(password)
                self.page.locator("input[name='PasswdAgain']").fill(password)
                logging.info("Password filled")
                next_button.click()

                self.page.wait_for_selector("input#phoneNumberId", timeout=DEFAULT_WAIT_TIME)
                self.page.locator("input#phoneNumberId").clear()
                self.page.fill("input#phoneNumberId", str(PHONE_NUMBER_AND_ID[0]))
                logging.info(f"Phone number filled: {str(PHONE_NUMBER_AND_ID[0])}")
                next_button.click()

                self.page.wait_for_selector("input#code", timeout=DEFAULT_WAIT_TIME)

                verification_code = get_verification_code()

                if verification_code:
                    self.page.locator("input#code").clear()
                    self.page.fill("input#code", verification_code)
                    next_button.click()
                    logging.info(f"Verification code filled successfully: {verification_code}")
                else:
                    logging.error(f"Error to fill verification code: {verification_code}")
            except PlaywrightTimeoutError as e:
                logging.error(f"Timeout encountered: {e}")
                return False
        except Exception as e:
            logging.error(f"Error creating email account: {email}")
            return False

    def close(self):
        if self.browser:
            self.browser.close()
            logging.info("Browser closed successfully")

def main():
    db = connect_db()
    if not db:
        logging.error("Failed to connect to database")
        return
    
    emails = fetch_emails(db)

    if not emails:              
        logging.error("No emails found for processing")
        db.close()
        return
    
    automation = None
    try:
        automation = EmailAutomation(proxy=None, proxy_username="gabrielmanna1994@gmail.com", proxy_password="QGN@bh2YJYLQxM8")
        for entry in emails:
            email = entry['email']
            password = entry['senha']
            gmail = entry['primeiro_nome']
            if not automation.create_email_account(email, gmail, password):
                logging.warning(f"Failed to create email {email}. Moving to next.")
    finally:
        if automation:
            automation.close()
        db.close()

if __name__ == "__main__":
    main()
