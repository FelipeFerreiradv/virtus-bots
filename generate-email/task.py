import mysql.connector
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from faker import Faker
import mysql.connector
from twilio.rest import Client
import imaplib
import email
from env import TWILIO_SECRET_KEY

print("Arquivo task.py carregado...")

# connect a databse 
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="bot_email_generate"
)

cursor = db.cursor()

print(cursor)

# function to save a emails in databse
def save_email(email, senha):
    cursor.execute("INSERT INTO emails (email, senha) VALUES (%s, %s)", (email, senha))
    db.commit()

# generate emails with Faker
def generate_emails(base_email, amount):
    emails_generated = []
    for i in range(amount):
        new_email = f"{base_email}@gmail.com"
        senha = Faker().password()
        save_email(new_email, senha)
        emails_generated.append((new_email, senha))
    print(emails_generated)
    return emails_generated

# examples of uses
emails = generate_emails("felipe123", 10)
for email, senha in emails:
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