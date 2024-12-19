import mysql.connector
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from faker import Faker
import mysql.connector
import imaplib
import email
import random

# Conectar ao banco de dados
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="bot_email_generate"
)

cursor = db.cursor()

print(cursor)

# Função para salvar e-mails no banco de dados
def save_email(email, senha):
    cursor.execute("INSERT INTO emails (email, senha) VALUES (%s, %s)", (email, senha))
    db.commit()

# Gerar e-mails com base em um nome e quantidade solicitada
def generate_emails(base_email, amount):
    emails_generated = []
    for i in range(amount):
        # Garantir que o e-mail seja único
        new_email = f"{base_email}{random.randint(1000, 9999)}@gmail.com"
        senha = Faker().password()
        save_email(new_email, senha)
        emails_generated.append((new_email, senha))
    print(emails_generated)
    return emails_generated

# Listas de nomes e sobrenomes
email_names = [
    "Ana", "Maria", "Beatriz", "Julia", "Gabriela", "Sophia", "Alice", "Isabela",
    "Carla", "Patricia", "Fernanda", "Larissa", "Amanda", "Luana", "Camila", "Thais",
    "Clara", "Valentina", "Rafaela", "Bianca", "Renata", "Eduarda", "Leticia", "Mariana",
    "Luiza", "Yasmin", "Tatiana", "Monica", "Debora", "Flavia", "Cristina", "Diana", "Raquel",
    "Nathalia", "Marta", "Bruna", "Tania", "Carolina", "Jessica", "Lorena", "Milena", "Sabrina",
    "Helena", "Daniela", "Ingrid", "Veronica", "Juliana", "Emily", "Sarah", "Olivia", "Emma",
    "Charlotte", "Ava", "Sofia", "Mia", "Isabella", "Amelia", "Harper", "Evelyn", "Abigail",
    "Scarlett", "Victoria", "Madison", "Luna", "Grace", "Zoe", "Addison", "Aubrey", "Ellie",
    "Stella", "Lucy", "Chloe", "Natalie", "Hannah", "Lily", "Savannah", "Elizabeth", "Aria", "Brooklyn"
]

email_surnames = [
    "Silva", "Santos", "Oliveira", "Pereira", "Costa", "Martins", "Gomes",
    "Almeida", "Lima", "Ferreira", "Rodrigues", "Barbosa", "Carvalho", "Sousa",
    "Araujo", "Ribeiro", "Moreira", "Moraes", "Castro", "Mendes", "Cardoso", "Campos",
    "Nogueira", "Batista", "Dias", "Freitas", "Teixeira", "Cavalcanti", "Pinheiro", "Macedo", "Monteiro",
    "Borges", "Magalhaes", "Vieira", "Goncalves", "Fonseca", "Barros", "Farias", "Santana", "Miranda",
    "Assis", "Amaral", "Coelho", "Soares", "Correia", "Braga", "Johnson", "Williams", "Brown", "Jones",
    "Miller", "Davis", "Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson",
    "Anderson", "Thomas", "Taylor", "Moore", "Martin", "Jackson", "White", "Harris", "Clark", "Lewis", "Young",
    "Hall", "Scott", "Allen", "Walker", "King", "Wright", "Green", "Adams", "Nelson", "Hill", "Ramirez",
    "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Parker", "Collins", "Edwards", "Stewart",
    "Morris", "Morgan"
]

# Gerar 10 e-mails únicos
email_count = 10
emails_to_generate = []

# Gerar 10 e-mails únicos
for i in range(email_count):
    draw_email_name = random.choice(email_names)
    draw_email_surname = random.choice(email_surnames)
    base_email = f"{draw_email_name}{draw_email_surname}{random.randint(100, 999)}"
    emails = generate_emails(base_email, 1)  # Gerar apenas um e-mail por vez
    emails_to_generate.extend(emails)  # Adicionar aos e-mails gerados

# Exibir e-mails e senhas gerados
for email, senha in emails_to_generate:
    print(f"Email: {email}, Senha: {senha}")

# # credentials of ot 

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

# # function to mark as verified
# def mark_as_verified(email):
#     cursor.execute("UPDATE emails SET status = 'usado' WHERE email = %s", (email,))
#     db.commit()