import mysql.connector
import random
import requests
from faker import Faker
import imaplib
import email

# Function to get proxy information via API
def get_proxy_info(proxy):
    parts = proxy.split(":")
    ip = parts[0]

    response = requests.get(f"https://ipinfo.io/{ip}/json")

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# connect with database
try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="bot_email_generate"
    )
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)

cursor = db.cursor()

# save emails and generate
def save_email(email, senha):
    cursor.execute("INSERT INTO emails (email, senha) VALUES (%s, %s)", (email, senha))
    db.commit()

def generate_emails(base_email, amount):
    emails_generated = []
    for i in range(amount):
        # Garantir que o e-mail seja único
        new_email = f"{base_email}{random.randint(1000, 9999)}@gmail.com"
        senha = Faker().password()
        save_email(new_email, senha)
        emails_generated.append((new_email, senha))
    return emails_generated

# main function
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

        # Lista de nomes e sobrenomes
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
        
        # Gerar os e-mails
        for i in range(email_count):
            draw_email_name = random.choice(email_names)
            draw_email_surname = random.choice(email_surnames)
            base_email = f"{draw_email_name}{draw_email_surname}{random.randint(100, 999)}"
            emails = generate_emails(base_email, 1)
            emails_to_generate.extend(emails)
        
        # Exibir os e-mails gerados
        for email, senha in emails_to_generate:
            print(f"Email: {email}, Senha: {senha}")
        
        # Retornar todas as informações geradas como um dicionário
        return {
            "proxy_info": proxy_info,
            "emails": [{"email": email, "senha": senha} for email, senha in emails_to_generate]
        }
    else:
        print("Não foi possível obter informações do proxy.")
        return None

# calls main functions
email_count = 10
proxy = "123.45.67.89"
result = generate_email_and_proxy(proxy, email_count)

if result:
    print("\nInformações Geradas:")
    print(result)

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