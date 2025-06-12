# Flask 

This Flask web application collects form submissions and displays them on a webpage.

## Features Covered:
- **Flask Setup**: Basic Flask application structure with a route (`/`).
- **Form Handling**: Accepts user input (`name`, `email`, `message`) via POST requests.
- **Data Storage**: Stores submissions temporarily in memory (list-based).
- **Timestamp Logging**: Records the time each submission is made.
- **HTML Rendering**: Displays submitted data dynamically on the webpage.

# FastAPI

- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **Pydantic**: Data validation and parsing using Python type annotations.
- **BaseModel**: Defines a structured model for employee data.
- **List Data Structure**: Stores employee records in memory.
- **CRUD Operations**:
  - `GET` - Fetch all employees.
  - `POST` - Add a new employee.
  - `PUT` - Update an existing employee by ID.
  - `DELETE` - Remove an employee by ID.
- **Path and Query Parameters**:
  - `/allEmp/{emp_id}` - Handles dynamic employee IDs in routes.
- **Basic Error Handling**: Checks if an employee exists before updating or deleting.


