import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from task import get_phone_number, get_verification_code, fetch_emails, connect_db, save_email
import time
import logging

GOOGLE_SIGNUP_URL = "https://accounts.google.com"
PROXY_SERVER = "rotating.proxyempire.io:9000:ukGDVRlSLkZYfG4A:mobile;us;;;"
DEFAULT_WAIT_TIME = 30

def generate_emails_automated(email, senha, primeiro_nome, sobrenome, proxy=None,):
    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    try:
        driver = webdriver.Firefox(options=options)
        logging.info("Navegador inicializado com sucesso.")
    except WebDriverException as e:
        logging.error(f"Erro ao inicializar o navegador: {e}")



    except Exception as e:
        logging.error(f"Erro inesperado ao criar a conta {email}: {e}")
        return False
    