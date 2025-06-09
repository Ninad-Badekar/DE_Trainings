from dotenv import load_dotenv
import os
import pymysql
import logging
import pandas as pd
logging.basicConfig(
    filename='window_functions_logs',
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

logging.info("✅ Connected successfully!")

queries = {
    "Q1_Total_Avg_Salary_Per_Department": """
        SELECT 
            employee_id, salary,
            SUM(salary) OVER (PARTITION BY department_id) AS dept_total,
            AVG(salary) OVER (PARTITION BY department_id) AS dept_avg
        FROM employees;
    """,
    "Q2_Top_3_Earners_Per_Department": """
        SELECT employee_id, first_name, department_id, ranknumber
        FROM (
            SELECT 
                employee_id,
                first_name,
                department_id,
                ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS ranknumber
            FROM employees
        ) AS ranked_emps
        WHERE ranknumber < 4;
    """,
    "Q3_Dense_Rank_By_Salary": """
        SELECT employee_id, salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS salary_rank
        FROM employees;
    """,
    "Q4_Salary_Quartiles": """
        SELECT employee_id, salary, NTILE(4) OVER (ORDER BY salary DESC) AS quartile
        FROM employees;
    """,
    "Q5_Lag_Lead_Salary_Per_Department": """
        SELECT
            employee_id,
            first_name,
            department_id,
            salary,
            LAG(salary) OVER (
                PARTITION BY department_id
                ORDER BY salary DESC
            ) AS prev_salary,
            LEAD(salary) OVER (
                PARTITION BY department_id
                ORDER BY salary DESC
            ) AS next_salary
        FROM employees;
    """
}

with connection.cursor() as cursor:
    for title, query in queries.items():
        logging.info(f"\n--- {title} ---")
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            logging.info(row)


