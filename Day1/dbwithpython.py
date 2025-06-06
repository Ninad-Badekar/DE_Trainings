import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="ninad123",
    database="de_training"
)

cursor = connection.cursor()

create_query = """
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20),
    age INT,
    department VARCHAR(20)
)
"""
cursor.execute(create_query)

insert_query = """
INSERT INTO employees (name, age, department)
VALUES (%s, %s, %s)
"""
sample_data = [
    ('Ninad', 24, 'Data Engineering'),
    ('Hariom', 22, 'Analytics'),
    ('Om', 23, 'Web Development'),
    ('Sahil', 25, 'DevOps'),
    ('Mihir', 21, 'Cloud Computing')
]
cursor.executemany(insert_query, sample_data)

connection.commit()

cursor.execute("SELECT * FROM employees")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
connection.close()
