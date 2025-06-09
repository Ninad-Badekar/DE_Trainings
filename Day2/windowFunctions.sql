use de_training;

#Q1: In your employees table, calculate the total salary and average salary per department, then show each employee’s salary along with those values.
SELECT 
  employee_id, salary,
  SUM(salary) OVER (PARTITION BY department_id) AS dept_total,
  AVG(salary) OVER (PARTITION BY department_id) AS dept_avg
FROM employees;

-- Q: Assign a unique sequential number to each employee within each department,
--  ordered by descending salary. Filter this list to only show the top 3 earners per department.
SELECT employee_id, first_name, department_id,ranknumber
FROM (
    SELECT 
      employee_id,
      first_name,department_id,
      ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS ranknumber
    FROM employees
) AS ranked_emps
WHERE ranknumber < 4;

-- Q:rank employees by salary (highest first), but handle ties:
select employee_id, salary , dense_rank() over(order by salary desc) from employees;

-- Q: Divide employees into 4 salary quartiles across the entire company, and output employee_id, salary, and their quartile number.
select employee_id,salary, ntile(5) over(order by salary desc) as quartile from employees; 

-- Q: For each department, compare each employee’s salary to the previous and next salary within that department when sorted by salary:

SELECT
  employee_id,
  first_name,
  department_id,
  salary,
  LAG(salary) OVER (
    PARTITION BY department_id
    ORDER BY salary DESC
  ) AS lags,
  LEAD(salary) OVER (
    PARTITION BY department_id
    ORDER BY salary DESC
  ) AS leads
FROM employees;


