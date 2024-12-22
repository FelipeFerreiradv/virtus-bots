import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from task import get_phone_number, get_verification_code, fetch_emails, connect_db, save_email
import smtplib
import imaplib
import pyautogui as pg
import time

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuração de constantes
GOOGLE_SIGNUP_URL = "https://accounts.google.com"
PROXY_SERVER = "rotating.proxyempire.io:9000:ukGDVRlSLkZYfG4A:mobile;us;;;"
DEFAULT_WAIT_TIME = 30


class EmailAutomation:
    def __init__(self, proxy=None):
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")  # Remove a detecção de automação
        options.add_argument("--disable-infobars")  # Remove a mensagem "Controlado por automação"
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option("useAutomationExtension", False)
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        
        try:
            self.driver = webdriver.Firefox(options=options)
            logging.info("Navegador inicializado com sucesso.")
        except WebDriverException as e:
            logging.error(f"Erro ao inicializar o navegador: {e}")
            raise

    def create_email_account(self, email, senha, primeiro_nome, sobrenome):
        driver = self.driver
        try:
            # Acessar página de criação de conta
            driver.get(GOOGLE_SIGNUP_URL)
            wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)

            # create a email button
            pg.press(['tab', 'tab', 'tab', 'tab'])
            pg.press("enter")
            time.sleep(3)
            pg.press("enter")

            # # Preenchimento de dados pessoais
            wait.until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(primeiro_nome)
            driver.find_element(By.ID, "lastName").send_keys(sobrenome)
            driver.find_element(By.CLASS_NAME, "VfPpkd-RLmnJb").click()
            # driver.find_element(By.NAME, "Passwd").send_keys(senha)
            # driver.find_element(By.NAME, "ConfirmPasswd").send_keys(senha)
            # driver.find_element(By.XPATH, "//span[text()='Próxima']").click()

            # # Adicionar número de telefone
            # phone_number = get_phone_number()
            # wait.until(EC.presence_of_element_located((By.ID, "phoneNumberId"))).send_keys(phone_number)
            # driver.find_element(By.XPATH, "//span[text()='Próxima']").click()

            # # Inserir código de verificação
            # verification_code = get_verification_code(phone_number)
            # wait.until(EC.presence_of_element_located((By.ID, "code"))).send_keys(verification_code)
            # driver.find_element(By.XPATH, "//span[text()='Próxima']").click()

            # Verificação de sucesso
            if "Bem-vindo" in driver.page_source:
                logging.info(f"Conta criada com sucesso: {email}")
                return True 
            else:
                logging.warning(f"Falha ao criar conta: {email}")
                return False

        except TimeoutException as e:
            logging.error(f"Erro de tempo limite durante a criação da conta {email}: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado ao criar a conta {email}: {e}")
            return False

    def close(self):
        self.driver.quit()
        logging.info("Navegador fechado com sucesso.")


def test_email_delivery(email, senha, recipient):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(email, senha)
            servidor.sendmail(email, recipient, "Teste de entrega de email.")
            logging.info(f"Email enviado com sucesso de {email} para {recipient}.")
            return True
    except Exception as e:
        logging.error(f"Erro ao enviar email de {email}: {e}")
        return False


def to_check_email(usuario, senha):
    try:
        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
            mail.login(usuario, senha)
            mail.select("inbox")
            logging.info(f"Login efetuado com sucesso para {usuario}.")
            return True
    except imaplib.IMAP4.error as e:
        logging.error(f"Falha no login para o email {usuario}: {e}")
        return False


def verify_emails_and_insert(email, senha, test_recipient, db):
    try:
        status = "no shadow ban" if test_email_delivery(email, senha, test_recipient) else "shadow ban"
        logging.info(f"Email {email} verificado. Status: {status}.")
        save_email(db, email, senha, status)
    except Exception as e:
        logging.error(f"Erro durante a verificação do email {email}: {e}")
        save_email(db, email, senha, "shadow ban")


def main():
    db = connect_db()
    if not db:
        logging.error("Falha ao conectar ao banco de dados.")
        return

    emails = fetch_emails(db)
    if not emails:
        logging.warning("Nenhum email encontrado para processamento.")
        db.close()
        return

    automation = None
    try:
        automation = EmailAutomation(proxy=PROXY_SERVER)
        # for entry in emails:
        #     email = entry['email']
        #     senha = entry['senha']
        #     primeiro_nome = entry['primeiro_nome']
        #     sobrenome = entry['sobrenome']
        #     if not automation.create_email_account(email, senha, primeiro_nome, sobrenome):
        #         logging.warning(f"Tentativa de criar email {email} falhou. Prosseguindo para o próximo.")
    finally:
        if automation:
            automation.close()
        db.close()


if __name__ == "__main__":
    main()


def test_email_delivery(email, senha, recipient):
    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(email, senha)
        message = "Teste de entrega de email."
        servidor.sendmail(email, recipient, message)
        servidor.quit()
        print(f"Email enviado com sucesso de {email} para {recipient}.")
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

# to check email
def to_check_email(usuario, senha):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(usuario, senha)
        mail.select("inbox")
        print("Login efetuado com sucesso.")
        return True
    except imaplib.IMAP4.error:
        print("Falha no login para o email.")
        return False
    
def verify_emails_and_insert(email, senha, test_recipient):
    try:
        login_is_sucess = test_email_delivery(email, senha, test_recipient)

        if login_is_sucess:
            status_shadow = "no shadow ban"
            print(f"Email {email} passou em todos os testes. Marcado como {status_shadow}.")
        else:
            status_shadow = "shadow ban"
            print(f"Falha no envio para o email: {email}. Marcado como {status_shadow}.")

        # Insert the email into the database with the status
        save_email(email, senha, status_shadow)
        return login_is_sucess
    except Exception as e:
        print(f"Erro durante a verificação do email {email}: {e}")
        status = "shadow ban"
        save_email(email, senha, status_shadow)
        return False