import mysql.connector
import random
import requests
from faker import Faker
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

def generate_emails(base_email, amount):
    """
    Gera uma lista de emails com senhas e os salva no banco de dados.
    """
    emails_generated = []
    for i in range(amount):
        new_email = f"{base_email}{random.randint(1000, 9999)}@gmail.com"
        senha = Faker().password()
        save_email(new_email, senha)
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
        emails = generate_emails(base_email, 10)
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

email_count = 10
emails = generate_email_set(email_count)
for email, senha in emails:
    print(f"Email: {email}, Senha: {senha}")


# # to check email
# def to_check_email(usuario, senha):
#     try:
#         mail = imaplib.IMAP4_SSL("imap.gmail.com")
#         mail.login(usuario, senha)
#         mail.select("inbox")
#         print("Login efetuado")
#     except imaplib.IMAP4.error:
#         print("Erro ao efetuar o login")
#         return 

#     # search for unread emails
#     try:
#         status, mensagens = mail.search(None, "UNSEEN")
#         if status != "OK":
#             print("Erro ao buscar emails não lidos.")
#             return

#         if mensagens[0]:
#             for num in mensagens[0].split():
#                 status, dados = mail.fetch(num, "(RFC822)")
#                 mensagem = email.message_from_bytes(dados[0][1])
#                 print(f"De: {mensagem['from']}")
#                 print(f"Assunto: {mensagem['subject']}")
#             print(f"Messages found")
#         else:
#             print("Nenhum email não lido encontrado.")
#     except Exception as e:
#         print(f"Erro ao buscar emails: {e}")
