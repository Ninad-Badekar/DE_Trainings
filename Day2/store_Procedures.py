import pymysql
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename="stored_procedures.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    autocommit=False
)

run_queries = {
    "CreateSalaryAuditTable": """
        CREATE TABLE IF NOT EXISTS salary_audit (
            audit_id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT,
            old_salary DECIMAL(10,2),
            new_salary DECIMAL(10,2),
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,

    "GetEmployeesByDepartment": """
        DROP PROCEDURE IF EXISTS GetEmployeesByDepartment;
        CREATE PROCEDURE GetEmployeesByDepartment(IN dept_id INT)
        BEGIN
            SELECT employee_id, first_name, salary
            FROM employees
            WHERE department_id = dept_id;
        END;
    """,

    "RaiseSalaryByDepartment": """
        DROP PROCEDURE IF EXISTS RaiseSalaryByDepartment;
        CREATE PROCEDURE RaiseSalaryByDepartment(
            IN dept_id INT,
            IN percent_increase DECIMAL(5,2)
        )
        BEGIN
            UPDATE employees
            SET salary = salary + (salary * percent_increase / 100)
            WHERE department_id = dept_id;
        END;
    """,

    "GetTopNEarnersByDepartment": """
        DROP PROCEDURE IF EXISTS GetTopNEarnersByDepartment;
        CREATE PROCEDURE GetTopNEarnersByDepartment(
            IN dept_id INT,
            IN top_n INT
        )
        BEGIN
            SELECT employee_id, first_name, salary
            FROM employees
            WHERE department_id = dept_id
            ORDER BY salary DESC
            LIMIT top_n;
        END;
    """,

    "UpdateSalaryWithAudit": """
        DROP PROCEDURE IF EXISTS UpdateSalaryWithAudit;
        CREATE PROCEDURE UpdateSalaryWithAudit(
            IN emp_id INT,
            IN new_salary DECIMAL(10,2)
        )
        BEGIN
            DECLARE old_salary DECIMAL(10,2);
            SELECT salary INTO old_salary FROM employees WHERE employee_id = emp_id;
            UPDATE employees
            SET salary = new_salary
            WHERE employee_id = emp_id;
            INSERT INTO salary_audit (employee_id, old_salary, new_salary)
            VALUES (emp_id, old_salary, new_salary);
        END;
    """
}

call_queries = {
    "GetEmployeesByDepartment": "CALL GetEmployeesByDepartment(90);",
    "RaiseSalaryByDepartment": "CALL RaiseSalaryByDepartment(90, 10.0);",
    "GetTopNEarnersByDepartment": "CALL GetTopNEarnersByDepartment(90, 3);",
    "UpdateSalaryWithAudit": "CALL UpdateSalaryWithAudit(101, 5000.00);"
}


def run_query(title):
    if title not in run_queries:
        logging.warning(f"Procedure '{title}' not found.")
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(run_queries[title])
            connection.commit()
            logging.info(f"Created: {title}")
    except Exception as e:
        logging.error(f"Failed to create: {title} — {e}")


def call_query(title):
    if title not in call_queries:
        logging.warning(f"Call '{title}' not found.")
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(call_queries[title])
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            logging.info(f"Called: {title}")
    except Exception as e:
        logging.error(f"Failed to call: {title} — {e}")



for proc_name in run_queries:
    run_query(proc_name)

call_query("GetEmployeesByDepartment")

connection.close()
