import os 
import logging
import pymysql
from dotenv import load_dotenv

logging.basicConfig(
    filename='views_logs',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT",3306))
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

logging.info("connected successfully")

queries = {
    "Create_View":"Create View people_with_no_managers as Select * from employees where manager_id is null",
    "Select_View": "Select * from people_with_no_managers",
    "Replace_View":"Create or Replace View people_with_no_managers as Select * from employees where manager_id =100",
    "Changed_View": "Select * from people_with_no_managers",
    "Drop_view":"Drop view if exists people_with_no_managers"
}

with connection.cursor() as cursor:
    for title,query in queries.items():
        logging.info(f"\n--- {title} ---")
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            logging.info(row)
