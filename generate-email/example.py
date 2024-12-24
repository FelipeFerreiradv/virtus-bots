import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from task import get_phone_number, get_verification_code, fetch_emails, connect_db, save_email
import time
import logging
import random

GOOGLE_SIGNUP_URL = "https://accounts.google.com"
PROXY_SERVER = "rotating.proxyempire.io:9000:ukGDVRlSLkZYfG4A:mobile;us;;;"
DEFAULT_WAIT_TIME = 50              

class EmailAutomation:
    def __init__(self, proxy=None):
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        options.add_argument("-private")
        options.add_argument("--disable-blink-features=AutomationControlled")  # Remove a detecção de automação
        options.add_argument("--disable-infobars")  # Remove a mensagem "Controlado por automação"
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        try:
            self.driver = webdriver.Firefox(options=options)
            logging.info("Navegador iniciado com sucesso")
        except WebDriverException as e:
            logging.error(f"Erro ao iniciar o navegador: {e}")
            raise

    def create_email_account(self, email, gmail, senha):
        driver = self.driver
        try:
            # open a google sign
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

            pg.press(["tab", "tab", "tab", "tab"])
            pg.press("enter")
            time.sleep(3)
            pg.press("enter")
            time.sleep(3)
            pg.write(f"{random.choice(email_names)}")
            pg.press("tab")
            pg.write(f"{random.choice(email_surnames)}")
            time.sleep(1)
            pg.press("tab") 
            pg.press("enter")
            time.sleep(3)
            pg.press("enter")
            time.sleep(5)
            pg.press("tab")
            pg.press("space")
            pg.press("down")
            pg.press("enter")    
            day_input = driver.find_element(By.ID, "day")
            day_input.send_keys(random.randint(1,30))
            year_input = driver.find_element(By.ID, "year")
            year_input.send_keys(random.randint(1940, 2000))
            pg.press("tab")
            pg.press("space")
            pg.press("down")
            pg.press("enter")
            pg.press(["tab", "tab"])
            pg.press("enter")
            time.sleep(5)
            gmail_input = driver.find_element(By.CLASS_NAME, "zHQkBf")
            gmail_input.send_keys(f"{gmail}")
            time.sleep(3)
            pg.press("tab")
            pg.press("enter")

            error_path = driver.find_element(By.CLASS_NAME, "dMNVAe")
            if error_path:
                pg.press("tab")
                pg.press("enter")

            multiple_emails = driver.find_element(By.ID, "selectionc4")
            if multiple_emails:
                pg.press("tab")
                pg.press("space")
                pg.press("tab")
                pg.press("enter")
                pg.write(f"{senha}")
                pg.press("tab")
                pg.write(f"{senha}")
                pg.press(["tab", "tab"])
                pg.press("enter")


        except TimeoutException as e:
            logging.error(f"Erro de tempo limite durante a criação da conta {email}: {e}")
            return False
        
        except Exception as e:
            logging.error(f"Erro inesperado ao criar a conta {email}: {e}")
            return False


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
            if not automation.create_email_account(email, gmail, senha):
                logging.warning(f"Tentativa de criar email {email} falhou. Prosseguindo para o próximo.")
    finally:
        if not automation:
            automation.close()
        db.close()

if __name__ == "__main__":
    main()
    