import mysql.connector
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("check_emails.log"), logging.StreamHandler()]
)

load_dotenv()
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "bot_email_generate")

def connect_db():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except MemoryError as e:
        logging.error(f"Error connect to database: {e}")
        return None
    
def fetch_emails_hinge():
    try:
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT email, senha, status_shadow FROM emails WHERE status_shadow = 'unknown'")
        emails = cursor.fetchall()

        updated_emails = []
        for email in emails:
            original_email = email['email']  # Alterado para 'email', que é o nome correto da chave no dicionário
            
            # Garantir que o email é do tipo Gmail (se necessário)
            if '@gmail.com' in original_email:
                prefix, domain = original_email.split('@')

                # Verifica se já existe um '+' no prefixo, se sim, ignora a mudança
                if '+' not in prefix:
                    # Adiciona o '+01' ao prefixo do email
                    new_email = f"{prefix}+01@{domain}"
                    updated_emails.append(new_email)

                    logging.debug(f"Email original: {original_email} -> Email alterado: {new_email}")
                else:
                    # Se já contiver '+', apenas mantém o email original
                    updated_emails.append(original_email)
            else:
                updated_emails.append(original_email)

        return updated_emails
    except mysql.connector.Error as e:
        logging.error(f"Erro ao buscar emails: {e}")
        return []
    
if __name__ == "__main__":
    db = connect_db()
    if db:
        try:
            fetch_emails_hinge()
        finally:
            db.close()
