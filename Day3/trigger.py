import logging
import pymysql
from db import get_connection 

conn_logger = logging.getLogger('connection')
conn_handler = logging.FileHandler('connection.log')
conn_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
conn_handler.setFormatter(conn_formatter)
conn_logger.addHandler(conn_handler)
conn_logger.setLevel(logging.INFO)

trigger_logger = logging.getLogger('trigger')
trigger_handler = logging.FileHandler('trigger.log')
trigger_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
trigger_handler.setFormatter(trigger_formatter)
trigger_logger.addHandler(trigger_handler)
trigger_logger.setLevel(logging.INFO)

pymysql_logger = logging.getLogger('pymysql')
pymysql_handler = logging.FileHandler('pymysql.log')
pymysql_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
pymysql_handler.setFormatter(pymysql_formatter)
pymysql_logger.addHandler(pymysql_handler)
pymysql_logger.setLevel(logging.WARNING)

# --- Trigger SQL ---
drop_update_trigger_sql = "DROP TRIGGER IF EXISTS after_employee_update;"
drop_insert_trigger_sql = "DROP TRIGGER IF EXISTS after_employee_insert;"
drop_delete_trigger_sql = "DROP TRIGGER IF EXISTS after_employee_delete;"

create_update_trigger_sql = """
CREATE TRIGGER after_employee_update
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
    INSERT INTO employee_logs (employee_id, first_name, action)
    VALUES (NEW.employee_id, NEW.first_name, 'updated');
END;
"""

create_insert_trigger_sql = """
CREATE TRIGGER after_employee_insert
AFTER INSERT ON employees
FOR EACH ROW
BEGIN
    INSERT INTO employee_logs (employee_id, first_name, action)
    VALUES (NEW.employee_id, NEW.first_name, 'inserted');
END;
"""

create_delete_trigger_sql = """
CREATE TRIGGER after_employee_delete
AFTER DELETE ON employees
FOR EACH ROW
BEGIN
    INSERT INTO employee_deletions (employee_id, first_name, last_name, email, deletion_time)
    VALUES (OLD.employee_id, OLD.first_name, OLD.last_name, OLD.email, NOW());
END;
"""

# --- Main Execution ---
try:
    conn = get_connection()
    conn_logger.info("Database connection established.")

    with conn.cursor() as cursor:
        # Drop existing triggers if they exist
        cursor.execute(drop_update_trigger_sql)
        cursor.execute(drop_insert_trigger_sql)
        cursor.execute(drop_delete_trigger_sql)
        trigger_logger.info("Dropped existing update, insert, and delete triggers if they existed.")

        # Create new triggers
        cursor.execute(create_update_trigger_sql)
        trigger_logger.info("Trigger 'after_employee_update' created successfully.")

        cursor.execute(create_insert_trigger_sql)
        trigger_logger.info("Trigger 'after_employee_insert' created successfully.")

        cursor.execute(create_delete_trigger_sql)
        trigger_logger.info("Trigger 'after_employee_delete' created successfully.")

        # Test update trigger
        employee_id_to_update = 100
        new_first_name = "Ninad"
        cursor.execute(
            "UPDATE employees SET first_name = %s WHERE employee_id = %s",
            (new_first_name, employee_id_to_update)
        )
        conn_logger.info(f"Updated employee_id={employee_id_to_update} first_name to '{new_first_name}'.")

        # Test insert trigger
        new_employee_data = {
            'first_name': 'TestFirst',
            'last_name': 'TestLast',
            'email': 'test@example.com',
            'phone_number': None,
            'hire_date': '2025-01-01',
            'job_id': 1,           # Replace with valid job_id from your jobs table
            'salary': 50000.00,
            'manager_id': None,
            'department_id': None
        }
        insert_sql = """
            INSERT INTO employees
            (first_name, last_name, email, phone_number, hire_date, job_id, salary, manager_id, department_id)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(hire_date)s,
                    %(job_id)s, %(salary)s, %(manager_id)s, %(department_id)s)
        """
        cursor.execute(insert_sql, new_employee_data)
        new_employee_id = cursor.lastrowid
        conn_logger.info(f"Inserted new employee with employee_id={new_employee_id}.")

        # Test delete trigger
        cursor.execute(
            "DELETE FROM employees WHERE employee_id = %s",
            (new_employee_id,)
        )
        conn_logger.info(f"Deleted employee_id={new_employee_id}.")

        # Check logs for update
        cursor.execute("SELECT * FROM employee_logs WHERE employee_id = %s", (employee_id_to_update,))
        update_logs = cursor.fetchall()
        if update_logs:
            trigger_logger.info(f"Update trigger log entries: {update_logs}")
        else:
            trigger_logger.warning(f"No update trigger log entries found for employee_id={employee_id_to_update}.")

        # Check logs for insert
        cursor.execute("SELECT * FROM employee_logs")
        insert_logs = cursor.fetchall()
        if insert_logs:
            trigger_logger.info(f"Insert trigger log entries: {insert_logs}")
        else:
            trigger_logger.warning(f"No insert trigger log entries found for employee_id={new_employee_id}.")

        # Check logs for delete
        cursor.execute("SELECT * FROM employee_deletions")
        delete_logs = cursor.fetchall()
        if delete_logs:
            trigger_logger.info(f"Delete trigger log entries: {delete_logs}")
        else:
            trigger_logger.warning(f"No delete trigger log entries found for employee_id={new_employee_id}.")

    conn.commit()

except pymysql.MySQLError as e:
    conn_logger.error(f"MySQL Error: {e}")
except Exception as ex:
    conn_logger.error(f"Unexpected error: {ex}")
finally:
    if conn:
        conn.close()
        conn_logger.info("Database connection closed.")
