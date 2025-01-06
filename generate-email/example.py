import logging
import random
import time
from task import generate_random_names, generate_random_surnames, get_phone_number, get_verification_code, fetch_emails, connect_db, save_email
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

GOOGLE_SIGNUP_URL = "https://accounts.google.com/signup"
PROXY_SERVER = "Itc6tLLIatUoR93k:wifi;us;;;newland@rotating.proxyempire.io:9000"
DEFAULT_WAIT_TIME = 5000
PHONE_NUMBER_AND_ID = get_phone_number()

class EmailAutomation:
    def __init__(self, proxy, proxy_username, proxy_password):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(
            headless=False,
            proxy={
                "server": proxy,
                "username": proxy_username,
                "password": proxy_password
                } if proxy else None
        )

        self.content = self.browser.new_context()
        self.page = self.content.new_page()
        logging.info("Browser opened")

    def create_email_account(self, email, gmail, password):
        try:
            # abrir página de signup do Google
            self.page.goto(GOOGLE_SIGNUP_URL)

            first_name = generate_random_names()
            last_name = generate_random_surnames()

            try:
                if not self.page.locator('input#day').is_visible():
                    self.page.fill('input#firstName', first_name)
                    self.page.fill('input#lastName', last_name)
                    next_button = self.page.get_by_role('button')
                    next_button_text = self.page.get_by_text("Next")
                    next_button.click()
                    logging.info(f"Filled: {first_name} {last_name}")

                self.page.get_by_label('Month').select_option("January")
                self.page.wait_for_selector('input#day', timeout=DEFAULT_WAIT_TIME)
                self.page.fill('input#day', str(random.randint(1,30)))
                self.page.fill("input#year", str(random.randint(1940, 2000)))
                gender_select = self.page.locator("select[id = 'gender']")
                gender_select.select_option(label="Rather not say")
                next_button.click()
                self.page.wait_for_load_state()
                self.page.wait_for_selector("input[name='Username']", timeout=DEFAULT_WAIT_TIME)
                self.page.locator("input[name='Username']").fill(gmail)
                logging.info("Input gmail filled")
                self.page.wait_for_selector("button", timeout=DEFAULT_WAIT_TIME)
                next_button_text.click(force=True)
                self.page.locator("input[name='Passwd']").fill(password)
                self.page.locator("input[name='PasswdAgain']").fill(password)
                logging.info("Password filled")
                next_button.click()

                # if self.page.get_by_text("Crie seu próprio endereço do Gmail"):
                #     self.page.get_by_text("Crie seu próprio endereço do Gmail").click()
                #     next_button_text.click()
                #     self.page.locator("input[name='Passwd']").fill(password)
                #     self.page.locator("input[name='PasswdAgain']").fill(password)
                #     logging.info("Password filled")
                #     next_button.click()

                #     self.page.locator("input#phoneNumberId", timeout=DEFAULT_WAIT_TIME)
                #     self.page.fill("input#phoneNumberId", str(get_phone_number()))
                #     logging.info(f"Phone number filled: {get_phone_number()}")
                #     next_button.click()
                # else:
                self.page.wait_for_selector("input#phoneNumberId", timeout=DEFAULT_WAIT_TIME)
                self.page.fill("input#phoneNumberId", str(PHONE_NUMBER_AND_ID[0]))
                logging.info(f"Phone number filled: {str(PHONE_NUMBER_AND_ID[0])}")
                next_button.click()

                try:
                    self.page.wait_for_selector("input#code", timeout=10000)
                    self.page.fill("input#code", get_verification_code())
                    next_button.click()
                except Exception as e:
                    logging.error(f"Error to fill code number: {e}")
            
            except PlaywrightTimeoutError as e:
                logging.error(f"Timeout encountered: {e}")
                return False
        except Exception as e:
            logging.error(f"Error ao criar conta de email: {email}")
            return False

    def close(self):
        if self.driver:
            self.driver.quit()
            logging.info("Navegador fechado com sucesso")

def main():
    db = connect_db()
    if not db:
        logging.error("Tentativa falha ao conectar-se com o banco de dados")
        return
    
    emails = fetch_emails(db)

    if not emails:              
        logging.error("Nenhum email encontrado para o processamento")
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
                logging.warning(f"Tentativa de criar email {email} falhou. Prosseguindo para o próximo.")
    finally:
        if automation:
            automation.close()
        db.close()

if __name__ == "__main__":
    main()
