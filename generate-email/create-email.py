from task import get_phone_number, get_verification_code, fetch_emails, connect_db, save_email
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
import imaplib
import smtplib

# Configuração do Selenium
class EmailAutomation:
    def __init__(self, proxy=None):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Executa em modo headless
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        self.driver = webdriver.Chrome(options=options)

    def create_email_account(self, email, senha, primeiro_nome, sobrenome):
        driver = self.driver

        try:
            # Acesse a página correta de criação de conta
            driver.get("https://accounts.google.com")
            wait = WebDriverWait(driver, 30)

            # Preencha os campos do formulário
            wait.until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(primeiro_nome)
            driver.find_element(By.ID, "lastName").send_keys(sobrenome)
            driver.find_element(By.ID, "username").send_keys(email.split("@")[0])
            driver.find_element(By.NAME, "Passwd").send_keys(senha)
            driver.find_element(By.NAME, "ConfirmPasswd").send_keys(senha)

            # Continue para adicionar o telefone
            driver.find_element(By.XPATH, "//span[text()='Próxima']").click()

            # Obter número de telefone e código de verificação
            phone_number = get_phone_number()
            wait.until(EC.presence_of_element_located((By.ID, "phoneNumberId"))).send_keys(phone_number)
            driver.find_element(By.XPATH, "//span[text()='Próxima']").click()

            verification_code = get_verification_code(phone_number)
            wait.until(EC.presence_of_element_located((By.ID, "code"))).send_keys(verification_code)
            driver.find_element(By.XPATH, "//span[text()='Próxima']").click()

            # Verifique o sucesso da conta
            if "Bem-vindo" in driver.page_source:
                print(f"Conta criada com sucesso: {email}")
                return True
            else:
                print(f"Falha ao criar conta: {email}")
                return False

        except Exception as e:
            print(f"Erro ao criar conta para {email}: {e}")
            return False

    def close(self):
        self.driver.quit()


# Processo principal
def main():
    db = connect_db()
    if not db:
        return  

    emails = fetch_emails(db)

    # Inicializar automação
    automation = EmailAutomation(proxy="rotating.proxyempire.io:9000:ukGDVRlSLkZYfG4A:mobile;us;;;")

    for entry in emails:
        email = entry['email']
        senha = entry['senha']
        primeiro_nome = entry['primeiro_nome']
        sobrenome = entry['sobrenome']

        success = automation.create_email_account(email, senha, primeiro_nome, sobrenome)
        if not success:
            print(f"Tentativa de criar email {email} falhou. Prosseguindo para o próximo.")

    # Finalizar automação
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