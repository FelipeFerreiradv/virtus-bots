import mysql.connector
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from faker import Faker
import mysql.connector
import imaplib
import email
import random

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
random_numbers = random.randint(100,200)
print(random_numbers)
email_names = [ 
    "Ana", "Maria", "Beatriz", "Julia", "Gabriela", "Sophia", "Alice", "Isabela", 
    "Carla", "Patricia", "Fernanda", "Larissa", "Amanda", "Luana", "Camila", "Thais",
    "Clara", "Valentina", "Rafaela", "Bianca", "Renata", "Eduarda", "Leticia", "Mariana",
    "Luiza", "Yasmin", "Tatiana", "Monica", "Debora", "Flavia", "Cristina", "Diana", "Raquel", 
    "Nathalia", "Marta", "Bruna", "Tania", "Carolina", "Jessica", "Lorena", "Milena", "Sabrina", 
    "Helena", "Daniela", "Ingrid", "Veronica", "Juliana",  "Emily", "Sarah", "Olivia", "Emma", "Charlotte", "Ava", "Sofia", "Mia",
    "Isabella", "Amelia", "Harper", "Evelyn", "Abigail", "Scarlett", "Victoria", "Madison",
    "Luna", "Grace", "Zoe", "Addison", "Aubrey", "Ellie", "Stella", "Lucy",
    "Chloe", "Natalie", "Hannah", "Lily", "Savannah", "Elizabeth", "Aria", "Brooklyn", 
     "Silva", "Santos", "Oliveira", "Pereira", "Costa", "Martins", "Gomes", 
    "Almeida", "Lima", "Ferreira", "Rodrigues", "Barbosa", "Carvalho", "Sousa", 
    "Araujo", "Ribeiro", "Moreira", "Moraes", "Castro", "Mendes", "Cardoso", "Campos",
    "Nogueira", "Batista", "Dias", "Freitas", "Teixeira", "Cavalcanti", "Pinheiro", "Macedo", "Monteiro", 
    "Borges", "Magalhaes", "Vieira", "Goncalves", "Fonseca", "Barros", "Farias", "Santana", "Miranda", 
    "Assis", "Amaral", "Coelho", "Soares", "Correia", "Braga",
    "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", 
    "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor",
    "Moore", "Martin", "Jackson", "White", "Harris", "Clark", "Lewis", "Young",
    "Hall", "Scott", "Allen", "Walker", "King", "Wright", "Green", "Adams", "Nelson",
    "Hill", "Ramirez", "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Parker", 
    "Collins", "Edwards", "Stewart", "Morris", "Morgan"
    ]
email_sumames = [
    "Silva", "Santos", "Oliveira", "Pereira", "Costa", "Martins", "Gomes", 
    "Almeida", "Lima", "Ferreira", "Rodrigues", "Barbosa", "Carvalho", "Sousa", 
    "Araujo", "Ribeiro", "Moreira", "Moraes", "Castro", "Mendes", "Cardoso", "Campos",
    "Nogueira", "Batista", "Dias", "Freitas", "Teixeira", "Cavalcanti", "Pinheiro", "Macedo", "Monteiro", 
    "Borges", "Magalhaes", "Vieira", "Goncalves", "Fonseca", "Barros", "Farias", "Santana", "Miranda", 
    "Assis", "Amaral", "Coelho", "Soares", "Correia", "Braga",
    "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", 
    "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor",
    "Moore", "Martin", "Jackson", "White", "Harris", "Clark", "Lewis", "Young",
    "Hall", "Scott", "Allen", "Walker", "King", "Wright", "Green", "Adams", "Nelson",
    "Hill", "Ramirez", "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Parker", 
    "Collins", "Edwards", "Stewart", "Morris", "Morgan"
]
complete_names = []
# loop name
for i in range(100):
    draw_email_names = random.choice(email_names)
    draw_email_sumnames = random.choice(email_sumames)
    complete_names_append = f"{draw_email_names}{draw_email_sumnames}{random_numbers}"
    complete_names.append(complete_names_append)
print(f"o nome sorteado foi {complete_names_append}")

emails = generate_emails(complete_names_append, 10)

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