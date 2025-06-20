import pymysql
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="ninad123",
    database="de_training"
)

tables = {
    "regions": """
        CREATE TABLE IF NOT EXISTS regions (
            region_id INT(11) AUTO_INCREMENT PRIMARY KEY,
            region_name VARCHAR(25) DEFAULT NULL
        )
    """,
    "countries": """
        CREATE TABLE IF NOT EXISTS countries (
            country_id CHAR(2) PRIMARY KEY,
            country_name VARCHAR(40) DEFAULT NULL,
            region_id INT(11) NOT NULL,
            FOREIGN KEY (region_id) REFERENCES regions(region_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        )
    """,
    "locations": """
        CREATE TABLE IF NOT EXISTS locations (
            location_id INT(11) AUTO_INCREMENT PRIMARY KEY,
            street_address VARCHAR(40) DEFAULT NULL,
            postal_code VARCHAR(12) DEFAULT NULL,
            city VARCHAR(30) NOT NULL,
            state_province VARCHAR(25) DEFAULT NULL,
            country_id CHAR(2) NOT NULL,
            FOREIGN KEY (country_id) REFERENCES countries(country_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        )
    """,
    "jobs": """
        CREATE TABLE IF NOT EXISTS jobs (
            job_id INT(11) AUTO_INCREMENT PRIMARY KEY,
            job_title VARCHAR(35) NOT NULL,
            min_salary DECIMAL(8,2) DEFAULT NULL,
            max_salary DECIMAL(8,2) DEFAULT NULL
        )
    """,
    "departments": """
        CREATE TABLE IF NOT EXISTS departments (
            department_id INT(11) AUTO_INCREMENT PRIMARY KEY,
            department_name VARCHAR(30) NOT NULL,
            location_id INT(11) DEFAULT NULL,
            FOREIGN KEY (location_id) REFERENCES locations(location_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        )
    """,
    "employees": """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INT(11) AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(20) DEFAULT NULL,
            last_name VARCHAR(25) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone_number VARCHAR(20) DEFAULT NULL,
            hire_date DATE NOT NULL,
            job_id INT(11) NOT NULL,
            salary DECIMAL(8,2) NOT NULL,
            manager_id INT(11) DEFAULT NULL,
            department_id INT(11) DEFAULT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs(job_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (department_id) REFERENCES departments(department_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
        )
    """,
    "dependents": """
        CREATE TABLE IF NOT EXISTS dependents (
            dependent_id INT(11) AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            relationship VARCHAR(25) NOT NULL,
            employee_id INT(11) NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        )
    """
}

cursor = conn.cursor()

try:
    for table_name, create_sql in tables.items():
        cursor.execute(create_sql)
        print(f"✅ Table '{table_name}' created successfully.")
    conn.commit()
finally:
    cursor.close()
    conn.close()
