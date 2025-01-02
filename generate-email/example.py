import logging
import random
import time
from task import get_phone_number, get_verification_code, fetch_emails, connect_db, save_email
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

GOOGLE_SIGNUP_URL = "https://accounts.google.com/signup"
PROXY_SERVER = "ukGDVRlSLkZYfG4A:senha:rotating.proxyempire.io:9000"
DEFAULT_WAIT_TIME = 5000

class EmailAutomation:
    def __init__(self, proxy):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,
            proxy={"server": proxy} if proxy else None
        )

        self.content = self.browser.new_context()
        self.page = self.content.new_page()
        logging.info("Browser opened")

    def create_email_account(self, email, gmail, password):
        try:
            # abrir página de signup do Google
            self.page.goto(GOOGLE_SIGNUP_URL)

            email_names = [
                "Ana", "Maria", "Beatriz", "Julia", "Gabriela", "Fernanda", "Carla", "Patricia", "Luana", "Rita",
                "Mariana", "Catarina", "Luciana", "Marta", "Juliana", "Vanessa", "Tania", "Simone", "Isabela", "Raquel",
                "Larissa", "Aline", "Tatiane", "Camila", "Monique", "Daniele", "Caroline", "Bianca", "Renata", "Elaine",
                "Lúcia", "Adriana", "Sandra", "Cristiane", "Sabrina", "Lilian", "Letícia", "Rosana", "Márcia", "Sílvia",
                "Natalia", "Priscila", "Cíntia", "Marina", "Verônica", "Michele", "Juliana", "Paula", "Kelly", "Cláudia",
                "Ester", "Joana", "Gláucia", "Rafaela", "Gabrielle", "Luciane", "Elaine", "Mariane", "Jéssica", "Kátia",
                "Thais", "Silvia", "Eliane", "Andreia", "Cleusa", "Vilma", "Lorena", "Roseli", "Sueli", "Neide", "Vera"
            ]
            email_surnames = [
                "Silva", "Santos", "Oliveira", "Pereira", "Costa", "Almeida", "Rodrigues", "Souza", "Lima", "Gomes",
                "Martins", "Fernandes", "Carvalho", "Melo", "Ribeiro", "Nascimento", "Araujo", "Dias", "Lopes", "Barbosa",
                "Ferreira", "Batista", "Castro", "Pinto", "Cavalcanti", "Vieira", "Freitas", "Moreira", "Teixeira", "Machado",
                "Queiroz", "Maciel", "Ramos", "Figueiredo", "Viana", "Moura", "Cunha", "Macedo", "Nunes", "Pereira", "Santos",
                "Tavares", "Marques", "Brito", "Gonçalves", "Zanetti", "Serrano", "Lima", "Rosa", "Brandão", "Azevedo", 
                "Pimentel", "Simões", "Cunha", "Barreto", "Pecanha", "Rochas", "Vasquez", "Farias", "Monteiro", "Martins",
                "Lopes", "Morais", "Correia", "Pinheiro", "Nascimento", "Dias", "Cunha", "Lima", "Barbosa", "Silveira",
                "Siqueira", "Salles", "Borges", "Assis", "Fonseca", "Valente", "Mota", "Fagundes", "Galvão", "Santiago", "Xavier",
                "Vilela", "Serrano", "Vieira", "Vargas", "Ribeiro", "Moreira", "Cavalcanti", "Tavares", "Pereira", "Pimentel"
            ]

            first_name = random.choice(email_names)
            last_name = random.choice(email_surnames)

            try:
                if not self.page.locator('input#day').is_visible():
                    self.page.fill('input#firstName', first_name)
                    self.page.fill('input#lastName', last_name)
                    next_button = self.page.get_by_role('button')
                    next_button_text = self.page.get_by_text("Próxima")
                    next_button.click()
                    logging.info(f"Filled: {first_name} {last_name}")

                self.page.wait_for_selector('input#day', timeout=DEFAULT_WAIT_TIME)
                self.page.fill('input#day', str(random.randint(1,30)))
                self.page.get_by_label('Mês').select_option("Janeiro")
                self.page.fill("input#year", str(random.randint(1940, 2000)))
                gender_select = self.page.locator("select[id = 'gender']")
                gender_select.select_option(label="Homem")
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

                if self.page.get_by_text("Crie seu próprio endereço do Gmail"):
                    self.page.get_by_text("Crie seu próprio endereço do Gmail").click()
                    next_button_text.click()
                    self.page.locator("input[name='Passwd']").fill(password)
                    self.page.locator("input[name='PasswdAgain']").fill(password)
                    logging.info("Password filled")
                    next_button.click()

                    try:
                        # self.page.wait_for_selector("input#phoneNumberId", timeout=DEFAULT_WAIT_TIME)
                        self.page.fill("input#phoneNumberId", str(get_phone_number()))
                        logging.info(f"Phone number filled: {get_phone_number()}")
                        next_button.click()
                    except Exception as e:
                        logging.erro(f"Not founded phone number {get_phone_number()}: {e}")

                try:
                    # self.page.wait_for_selector("input#phoneNumberId", timeout=DEFAULT_WAIT_TIME)
                    self.page.fill("input#phoneNumberId", str(get_phone_number()))
                    logging.info(f"Phone number filled: {get_phone_number()}")
                    next_button.click()
                except Exception as e:
                    logging.erro(f"Not founded phone number {get_phone_number()}: {e}")

                return False
            except PlaywrightTimeoutError as e:
                logging.error(f"Timeout encountered: {e}")
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
        automation = EmailAutomation(proxy=None)
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
