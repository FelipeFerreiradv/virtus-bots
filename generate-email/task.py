import mysql.connector
import random
import requests
from faker import Faker
from urllib.parse import quote
from dotenv import load_dotenv
import os
import time
import logging

# Configuração do logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("bot_email_generate.log"), logging.StreamHandler()]
)

# Carregar variáveis de ambiente
load_dotenv()
API_KEY_5SIM = os.getenv("API_KEY_5SIM")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "bot_email_generate")

# Instância global do Faker
faker = Faker()

# Funções auxiliares
def parse_proxy(proxy):
    try:
        parts = proxy.split(":")
        if len(parts) >= 4:
            host, port, username, password = parts[:4]
            username = quote(username)
            password = quote(password)
            return {
                "http": f"http://{username}:{password}@{host}:{port}",
                "https": f"http://{username}:{password}@{host}:{port}",
            }
        raise ValueError("Formato de proxy inválido.")
    except Exception as e:
        logging.error(f"Erro ao processar o proxy: {e}")
        return None

def get_proxy_info(proxy):
    proxies = parse_proxy(proxy)
    if not proxies:
        return None
    try:
        response = requests.get("https://ipinfo.io/json", proxies=proxies, timeout=20)
        response.raise_for_status()
        logging.info("Conexão bem-sucedida")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao conectar ao proxy: {e}")
        return None

def connect_db():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except mysql.connector.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def save_email(db, email, senha, status_shadow):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as count FROM emails WHERE email = %s", (email,))
        if cursor.fetchone()['count'] == 0:
            cursor.execute(
                "INSERT INTO emails (email, senha, status_shadow) VALUES (%s, %s, %s)",
                (email, senha, status_shadow)
            )
            db.commit()
            logging.info(f"Email {email} salvo com status: {status_shadow}.")
        else:
            logging.info(f"Email {email} já existe no banco de dados.")
    except mysql.connector.Error as e:
        logging.error(f"Erro ao salvar email no banco de dados: {e}")

def generate_random_names():
    email_names = [
    "Ana", "Maria", "Beatriz", "Julia", "Gabriela", "Fernanda", "Carla", "Patricia", "Luana", "Rita",
    "Mariana", "Catarina", "Luciana", "Marta", "Juliana", "Vanessa", "Tania", "Simone", "Isabela", "Raquel",
    "Larissa", "Aline", "Tatiane", "Camila", "Monique", "Daniele", "Caroline", "Bianca", "Renata", "Elaine",
    "Lúcia", "Adriana", "Sandra", "Cristiane", "Sabrina", "Lilian", "Letícia", "Rosana", "Márcia", "Sílvia",
    "Natalia", "Priscila", "Cíntia", "Marina", "Verônica", "Michele", "Juliana", "Paula", "Kelly", "Cláudia",
    "Ester", "Joana", "Gláucia", "Rafaela", "Gabrielle", "Luciane", "Elaine", "Mariane", "Jéssica", "Kátia",
    "Thais", "Silvia", "Eliane", "Andreia", "Cleusa", "Vilma", "Lorena", "Roseli", "Sueli", "Neide", "Vera"
    ]

    return random.choice(email_names)

def generate_random_surnames():
    email_surnames = [
    "Silva", "Santos", "Oliveira", "Pereira", "Costa", "Almeida", "Rodrigues", "Souza", "Lima", "Gomes",
    "Martins", "Fernandes", "Carvalho", "Melo", "Ribeiro", "Nascimento", "Araujo", "Dias", "Lopes", "Barbosa",
    "Ferreira", "Batista", "Castro", "Pinto", "Cavalcanti", "Vieira", "Freitas", "Moreira", "Teixeira", "Machado",
    "Queiroz", "Maciel", "Ramos", "Figueiredo", "Viana", "Moura", "Cunha", "Macedo", "Nunes", "Pereira", "Santos",
    "Tavares", "Marques", "Brito", "Gonçalves", "Zanetti", "Serrano", "Lima", "Rosa", "Brandão", "Azevedo", 
    "Pimentel", "Simões", "Cunha", "Barreto", "Pecanha", "Rochas", "Vasquez", "Farias", "Monteiro", "Martins",
    "Lopes", "Morais", "Correia", "Pinheiro", "Nascimento", "Dias", "Cunha", "Lima", "Barbosa", "Silveira",
    "Siqueira", "Salles", "Borges", "Assis", "Fonseca", "Valente", "Mota", "Fagundes", "Galvão", "Santiago", "Xavier",
    "Vilela", "Serrano", "Vieira", "Vargas", "Ribeiro", "Moreira", "Cavalcanti", "Tavares", "Pereira", "Pimentel"
    ]

    return random.choice(email_surnames)

def generate_random_countries():
    RANDOM_COUNTRIES = ["philippines", "ethiopia", "vietnam", "indonesia", "azerbaijan", "cambodia", "uzbekistan", "lithuania", "tanzania"]

    random_countries_values = random.choice(RANDOM_COUNTRIES)

    return random_countries_values

def generate_emails(base_email, amount, db):
    emails_generated = []
    for _ in range(amount):
        new_email = f"{base_email}{random.randint(1000, 9999)}@gmail.com"
        senha = faker.password()
        save_email(db, new_email, senha, "unknown")
        emails_generated.append((new_email, senha))
    logging.info(f"Total de emails gerados: {len(emails_generated)}")
    return emails_generated

def generate_email_set(email_count, db):
    emails_to_generate = []
    for _ in range(email_count):
        base_email = f"{generate_random_names()}{generate_random_surnames()}{random.randint(100, 999)}"
        emails = generate_emails(base_email, 5, db)
        emails_to_generate.extend(emails)
    return emails_to_generate

def fetch_emails(db):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT email, senha, status_shadow FROM emails WHERE status_shadow = 'unknown'")
        emails = cursor.fetchall()

        for email in emails:
            # Dividir o nome do email para garantir que o primeiro_nome e sobrenome estejam corretos
            nome_sobrenome = email['email'].split('@')[0]
            
            # Verificar se o nome_sobrenome contém um ponto
            if '.' in nome_sobrenome:
                nome, sobrenome = nome_sobrenome.split('.', 1)
            else:
                # Caso não tenha ponto, usar o mesmo valor para nome e sobrenome
                nome = nome_sobrenome
                sobrenome = ""

            email['primeiro_nome'] = nome
            email['sobrenome'] = sobrenome

        return emails
    except mysql.connector.Error as e:
        logging.error(f"Erro ao buscar emails: {e}")
        return []

def get_phone_number(product="google", country=f"brazil", operator="any"):
    try:
        headers = {
            'Authorization': f'Bearer {API_KEY_5SIM}',
            'Accept': 'application/json',
        }
           
        params={
            "country": country,
            "operator": operator,
            "product": product,
        }

        response = requests.get(
            f"https://5sim.net/v1/user/buy/activation/{country}/{operator}/{product}",
            headers=headers, 
            params=params
        )

        response.raise_for_status()

        data = response.json()

        phone = data.get('phone')
        id = data.get('id')
        
        logging.debug(f"Headers enviados: {headers}")
        logging.debug(f"Parametros enviados: {params}")
        logging.debug(f"Resposta completa enviados: {response.text}")
        if phone and id:
            logging.info(f"Número de telefone e id adquirido: {phone} | {id}")
            return phone, id
        logging.warning("Número de telefone e id não disponível.")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar número e id: {e}")
        print(response.text)
        return None

def get_verification_code():
    try:
        for attempt in range(20):
            phone, id = get_phone_number()

            if not id:
                logging.error("Error to found number id")

            headers = {
            'Authorization': f'Bearer {API_KEY_5SIM}',
            'Accept': 'application/json',
            }

            response = requests.get(
                f'https://5sim.net/v1/user/check/{id}', headers=headers
            )
            response.raise_for_status()

            data = response.json()

            if 'sms' in data and len(data['sms']) > 0:
                verification_code = data['sms'][0]['code']
                logging.info(f"Código de verificação recebido: {verification_code}")
                return verification_code
            
            logging.info(f"Attempt {attempt + 1}: Code not received. Waiting 10 seconds...")
            time.sleep(10)

        logging.warning("Code not received after 10 seconds")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar código: {e}")
        return None

if __name__ == "__main__":
    db = connect_db()
    if db:
        try:
            generate_email_set(2, db)
        finally:
            db.close()