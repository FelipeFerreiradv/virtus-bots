import mysql.connector
import random
import requests
from faker import Faker
import imaplib
import email
from urllib.parse import quote


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


def save_email(email, senha):
    cursor.execute("INSERT INTO emails (email, senha) VALUES (%s, %s)", (email, senha))
    db.commit()
    print(f"Email salvo: {email}")

    cursor.execute("SELECT email, senha FROM emails WHERE email = %s", (email,))
    result = cursor.fetchone()
    if result:
        print(f"Email recuperado: {result[0]}, Senha: {result[1]}")
    else:
        print("Erro ao salvar o email.")


def generate_emails(base_email, amount):
    emails_generated = []
    for i in range(amount):
        new_email = f"{base_email}{random.randint(1000, 9999)}@gmail.com"
        senha = Faker().password()
        save_email(new_email, senha)
        emails_generated.append((new_email, senha))
        print(f"Email gerado: {new_email}, Senha: {senha}")

    mostrar_emails()
    print(f"Total de emails gerados: {len(emails_generated)}")
    return emails_generated


def generate_email_and_proxy(proxy, email_count):
    emails_to_generate = []
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

        for i in range(email_count):
            draw_email_name = random.choice(email_names)
            draw_email_surname = random.choice(email_surnames)
            base_email = f"{draw_email_name}{draw_email_surname}{random.randint(100, 999)}"
            print(f"Base do email gerado: {base_email}")  # Confirma a base do email
            emails = generate_emails(base_email, 10)
            emails_to_generate.extend(emails)
        
        print(f"Total de emails gerados (final): {len(emails_to_generate)}")
        
        for email, senha in emails_to_generate:
            print(f"Email: {email}, Senha: {senha}")

        return {
            "proxy_info": proxy_info,
            "emails": [{"email": email, "senha": senha} for email, senha in emails_to_generate]
        }
    else:
        print("Não foi possível obter informações do proxy.")
        return None

# Configurações principais
email_count = 10
proxy = "rotating.proxyempire.io:9000:ukGDVRlSLkZYfG4A:mobile;us;;;"

proxy_info = get_proxy_info(proxy)

if proxy_info:
    print("Informações do Proxy:")
    print(proxy_info)
else:
    print("Não foi possível conectar ao proxy.")

def mostrar_emails():
    cursor.execute("SELECT email, senha FROM emails")  # Selecione apenas as colunas que você precisa
    emails = cursor.fetchall()

    if emails:
        print("Emails salvos no banco de dados:")
        for email, senha in emails:
            print(f"Email: {email}, Senha: {senha}")
    else:
        print("Nenhum email encontrado no banco de dados.")

# # to check email
# def to_check_email(usuario, senha):
#     mail = imaplib.IMAP4_SSL("imap.gmail.com")
#     mail.login(usuario, senha)
#     mail.select("inbox")
    
#     # Busca por emails não lidos
#     status, mensagens = mail.search(None, "UNSEEN")
#     for num in mensagens[0].split():
#         status, dados = mail.fetch(num, "(RFC822)")
#         mensagem = email.message_from_bytes(dados[0][1])
#         print(f"De: {mensagem['from']}")
#         print(f"Assunto: {mensagem['subject']}")