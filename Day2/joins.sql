use de_training;

# q1 List employees with their department names (exclude those without departments).
select employee_id,concat(first_name," ",last_name) as name ,department_name
from employees e inner join departments d on e.department_id = d.department_id;

#q2 Show all departments and any employees working in them (include departments with no employees).
select D.department_name,E.first_name From departments D
LEFT join employees E on E.department_id=D.department_id;

#q3 Find all employees and the location of their department 
#(including employees whose department might be missing a location
#).
SELECT E.first_name, E.last_name, L.city
FROM employees E
RIGHT JOIN departments D
  ON E.department_id = D.department_id
RIGHT JOIN locations L
  ON D.location_id = L.location_id;

#q4 List all departments and all employees — match them where possible, 
#plus include unmatched departments or employees.

SELECT E.employee_id, E.first_name, D.department_name
FROM employees E
LEFT JOIN departments D
  ON E.department_id = D.department_id

UNION ALL

SELECT E.employee_id, E.first_name, D.department_name
FROM employees E
RIGHT JOIN departments D
  ON E.department_id = D.department_id
WHERE E.department_id IS NULL;

# q5 Find all pairs of employees who share the same manager, listing both employee names. 
#Exclude pairing an employee with themselves.
select e1.employee_id as emp1 ,e2.employee_id as emp2 , e1.manager_id
from employees e1 join
employees e2 on e1.manager_id = e2.manager_id 
WHere e1.employee_id < e2.employee_id;

# q6 List all departments that currently have no employees assigned 
#(i.e., departments present in departments but absent in employees). 
SELECT d.department_id, d.department_name
FROM departments d
LEFT JOIN employees e
  ON d.department_id = e.department_id
WHERE e.employee_id IS NULL;

#q7 Identify all locations that are not referenced by any department
# (i.e., locations with no departments at that site). Write this using NOT EXISTS subquery .
SELECT l.location_id, l.city
FROM locations l
WHERE NOT EXISTS (
  SELECT 1
  FROM departments d
  WHERE d.location_id = l.location_id
);

