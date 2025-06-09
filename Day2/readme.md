# 📘 SQL Concepts Overview: Stored Procedures, Views, and Window Functions

## 👨‍💻 About This Document

This document summarizes the key SQL concepts I have learned and practiced, specifically focused on:

- Stored Procedures
- Views
- Window Functions

It includes descriptions, sample use cases, and real examples I implemented during my learning process.

---

## ⚙️ 1. Stored Procedures

### ✅ What I Learned
- Stored Procedures are saved SQL code that can be reused and executed repeatedly.
- Useful for encapsulating business logic in the database.
- Help in reducing client-server communication and improve performance.

### 🧪 Example

```sql
DELIMITER //
CREATE PROCEDURE GetEmployeeByDept(IN dept_id INT)
BEGIN
    SELECT employee_id, first_name, salary
    FROM employees
    WHERE department_id = dept_id;
END //
DELIMITER ;

## 🔍 2. Views

### ✅ What I Learned

- A view is a virtual table created using a `SELECT` query.
- Helps abstract and simplify complex queries.
- Enhances data security by limiting column-level access.

### 🧪 Example

```sql
CREATE VIEW high_salary_employees AS
SELECT employee_id, first_name, salary
FROM employees
WHERE salary > 10000;

## 📊 3. Window Functions

### ✅ What I Learned

- Window functions allow you to perform calculations across a set of rows related to the current row.
- Unlike aggregate functions, they do not collapse rows into a single output.
- Great for analytics and row-wise comparison within partitions.

### ✨ Key Functions

- `ROW_NUMBER()`
- `RANK()`
- `DENSE_RANK()`
- `LAG()`
- `LEAD()`

### 🧪 Example 1: Rank Employees by Salary within Department

```sql
SELECT 
    employee_id,
    department_id,
    salary,
    RANK() OVER(PARTITION BY department_id ORDER BY salary DESC) AS rank_in_dept
FROM employees;


## 🛠️ Tools & Technologies Used

- **MySQL** – for relational database queries  
- **PyMySQL** – for connecting MySQL with Python  
- **MySQL Workbench** – for visual database management  
- **.env files** – for secure DB credential storage  
- **Python Logging** – for execution tracking  
