from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging
import time
import random
from task import get_phone_number, get_verification_code, fetch_emails, connect_db, save_email

GOOGLE_SIGNUP_URL = "https://accounts.google.com/signup"
PROXY_SERVER = "rotating.proxyempire.io:9000:ukGDVRlSLkZYfG4A:mobile;us;;;"
DEFAULT_WAIT_TIME = 120

class EmailAutomation:
    def __init__(self, proxy):
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        options.add_argument("--disable-automation")
        options.add_argument("--disable-blink-features=AutomationControlled")  # Remove a detecção de automação
        options.add_argument("--disable-infobars")  # Remove a mensagem "Controlado por automação"
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("-private")
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        try:
            service = Service(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=options)
            logging.info("Navegador iniciado com sucesso")
        except WebDriverException as e:
            logging.error(f"Erro ao iniciar o navegador: {e}")
            raise

    def create_email_account(self, email):
        driver = self.driver
        try:
            # abrir página de signup do Google
            driver.get(GOOGLE_SIGNUP_URL)
            wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)

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

            try:
                time.sleep(3)
                first_name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='firstName']")))
                first_name_input.clear()
                first_name_input.send_keys(random.choice(email_names))
                last_name_input = wait.until(EC.presence_of_element_located((By.ID, "lastName")))
                last_name_input.clear()
                last_name_input.send_keys(random.choice(email_surnames))
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
                next_button.click()
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                next_button.click()
            except TimeoutException as e:
                logging.error(f"Timeout ao tentar encontrar o botão 'Next': {e}")
                driver.save_screenshot("timeout_next_button.png")
                return False
            except Exception as e:
                logging.error(f"Erro ao interagir com o botão 'Next': {e}")
                driver.save_screenshot("unexpected_error_next_button.png")
                return False
        except Exception as e:
            logging.error(f"Erro ao criar conta de email: {email}")
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
        automation = EmailAutomation(proxy=PROXY_SERVER)
        for entry in emails:
            email = entry['email']
            senha = entry['senha']
            gmail = entry['primeiro_nome']
            if not automation.create_email_account(email):
                logging.warning(f"Tentativa de criar email {email} falhou. Prosseguindo para o próximo.")
    finally:
        if automation:
            automation.close()
        db.close()

if __name__ == "__main__":
    main()
