import pymysql.cursors

# Connect to the database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='ninad123',
    database='de_training',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Define all seven queries
queries = {
    'q1_emps_with_dept': """
        SELECT employee_id, 
               CONCAT(first_name, ' ', last_name) AS name, 
               department_name
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.department_id;
    """,
    'q2_depts_with_emps': """
        SELECT d.department_id, d.department_name, e.first_name
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id;
    """,
    'q3_emps_with_dept_loc': """
        SELECT e.employee_id, e.first_name, e.last_name, l.city
        FROM employees e
        RIGHT JOIN departments d ON e.department_id = d.department_id
        RIGHT JOIN locations l ON d.location_id = l.location_id;
    """,
    'q4_full_outer_emps_depts': """
        SELECT e.employee_id, e.first_name, d.department_name
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.department_id
        UNION ALL
        SELECT e.employee_id, e.first_name, d.department_name
        FROM employees e
        RIGHT JOIN departments d ON e.department_id = d.department_id
        WHERE e.department_id IS NULL;
    """,
    'q5_pairs_same_manager': """
        SELECT e1.employee_id AS emp1,
               e2.employee_id AS emp2,
               e1.manager_id
        FROM employees e1
        JOIN employees e2
          ON e1.manager_id = e2.manager_id
        WHERE e1.employee_id < e2.employee_id;
    """,
    'q6_depts_no_emps': """
        SELECT d.department_id, d.department_name
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id
        WHERE e.employee_id IS NULL;
    """,
    'q7_locations_no_dept': """
        SELECT l.location_id, l.city
        FROM locations l
        WHERE NOT EXISTS (
            SELECT 1
            FROM departments d
            WHERE d.location_id = l.location_id
        );
    """
}


with conn:
    with conn.cursor() as cursor:
        # Loop through each query
        for label, sql in queries.items():
            print(f"\n=== {label} ===")
            cursor.execute(sql)  # best practice: one statement at a time :contentReference[oaicite:0]{index=0}
            rows = cursor.fetchall()
            print(f"Rows returned: {len(rows)}")
            for row in rows:
                print(row)
                
