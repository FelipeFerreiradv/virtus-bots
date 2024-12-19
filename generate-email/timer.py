import schedule
import time
import logging
from task import generate_emails, to_check_email

# configuring of logs
logging.basicConfig(
    filename="task_scheduler.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def job():
    try:
        logging.info("Iniciando tarefa de geração e verificação de emails...")
        generate_emails()
        logging.info("Emails gerados com sucesso.")
        
        to_check_email()
        logging.info("Verificação de emails concluída.")
    except Exception as e:
        logging.error(f"Erro ao executar tarefa: {e}")

# scheduling of day task
schedule.every().day.at("19:00").do(job)

logging.info("Scheduler iniciado. Aguardando a execução da tarefa...")

# Loop 
while True:
    try:
        schedule.run_pending()
    except Exception as e:
        logging.error(f"Erro ao processar o agendamento: {e}")
    time.sleep(1)
