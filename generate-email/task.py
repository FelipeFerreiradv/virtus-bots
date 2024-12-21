import mysql.connector
import random
import requests
from faker import Faker
import email
from urllib.parse import quote
import imaplib
import smtplib



def parse_proxy(proxy):
    """
    Function to process proxy format (host:port:username:password)
    and return a dictionary of proxies.
    """
    try:
        host, port, username, password = proxy.split(":")
        # Encode username and password for special characters
        username = quote(username)
        password = quote(password)

        proxies = {
            "http": f"http://{username}:{password}@{host}:{port}",
            "https": f"http://{username}:{password}@{host}:{port}",
        }
        return proxies
    except Exception as e:
        print(f"Erro ao processar o proxy: {e}")
        return None

def get_proxy_info(proxy):
    """
    Get proxy information using the IPinfo API.
    """
    proxies = parse_proxy(proxy)
    if not proxies:
        print("Erro ao formatar o proxy.")
        return None

    try:
        response = requests.get("https://ipinfo.io/json", proxies=proxies, timeout=20)
        response.raise_for_status()  # Lança exceção se houver erro HTTP
        print("Conexão bem-sucedida")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ao proxy: {e}")
        return None

# Conexão com o banco de dados
try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="bot_email_generate"
    )
    print("Conexão com o banco de dados bem-sucedida!")
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)

cursor = db.cursor()

def save_email(email, senha, status_shadow):
    """
    Inserts the email into the database with the specified status.
    """
    try:
        cursor.execute("INSERT INTO emails (email, senha, status_shadow) VALUES (%s, %s, %s)", (email, senha, status_shadow))
        db.commit()
        print(f"Email {email} salvo com status: {status_shadow}.")
    except Exception as e:
        print(f"Erro ao salvar email no banco de dados: {e}")

def generate_emails(base_email, amount):
    """
    Gera uma lista de emails com senhas e os salva no banco de dados.
    """
    emails_generated = []
    for i in range(amount):
        new_email = f"{base_email}{random.randint(1000, 9999)}@gmail.com"
        senha = Faker().password()
        status = "unknown"
        save_email(new_email, senha, status)
        emails_generated.append((new_email, senha))
        print(f"Email gerado: {new_email}, Senha: {senha}")

    print(f"Total de emails gerados: {len(emails_generated)}")
    return emails_generated

def generate_email_set(email_count):
    """
    Função para criar e-mails e suas senhas com nomes fictícios.
    """
    email_names = [
        "Ana", "Maria", "Beatriz", "Julia", "Gabriela", "Sophia", "Alice", "Isabela",
        "Carla", "Patricia", "Fernanda", "Larissa", "Amanda", "Luana", "Camila", "Thais",
        "Clara", "Valentina", "Rafaela", "Bianca", "Renata", "Eduarda", "Leticia", "Mariana",
        "Luiza", "Yasmin", "Tatiana", "Monica", "Debora", "Flavia", "Cristina", "Diana", "Raquel"
    ]
    email_surnames = [
        "Silva", "Santos", "Oliveira", "Pereira", "Costa", "Martins", "Gomes", "Almeida",
        "Lima", "Ferreira", "Rodrigues", "Barbosa", "Carvalho", "Sousa", "Araujo", "Ribeiro"
    ]

    emails_to_generate = []
    for _ in range(email_count):
        draw_email_name = random.choice(email_names)
        draw_email_surname = random.choice(email_surnames)
        base_email = f"{draw_email_name}{draw_email_surname}{random.randint(100, 999)}"
        emails = generate_emails(base_email, 5)
        emails_to_generate.extend(emails)

    print(f"Total de emails gerados: {len(emails_to_generate)}")
    return emails_to_generate

def process_proxy(proxy):
    """
    Processa as informações do proxy e exibe detalhes sobre sua localização e provedor.
    """
    proxy_info = get_proxy_info(proxy)

    if proxy_info:
        print("Informações do Proxy:")
        print(f"IP: {proxy_info['ip']}")
        print(f"Cidade: {proxy_info.get('city', 'N/A')}")
        print(f"Região: {proxy_info.get('region', 'N/A')}")
        print(f"País: {proxy_info.get('country', 'N/A')}")
        print(f"Organização: {proxy_info.get('org', 'N/A')}")
        print(f"Código Postal: {proxy_info.get('postal', 'N/A')}")
        print(f"Timezone: {proxy_info.get('timezone', 'N/A')}")
        return proxy_info
    else:
        print("Não foi possível obter informações do proxy.")
        return None

# Uso separado das funções
proxy = "rotating.proxyempire.io:9000:ukGDVRlSLkZYfG4A:mobile;us;;;"
proxy_info = process_proxy(proxy)

if proxy_info:
    print("Informações do proxy obtidas com sucesso.")
else:
    print("Erro ao obter informações do proxy.")

email_count = 3
emails = generate_email_set(email_count)
for email, senha in emails:
    print(f"Email: {email}, Senha: {senha}")

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