
import pymysql
import os
from dotenv import load_dotenv
import logging
db_logger = logging.getLogger('db')
db_handler = logging.FileHandler('connection.log')
db_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
db_handler.setFormatter(db_formatter)
db_logger.addHandler(db_handler)
db_logger.setLevel(logging.INFO)

load_dotenv()

def get_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        logging.info("Error connecting to database:", e)
        raise
