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

# Django Concepts Overview

Django is a high-level Python web framework that enables rapid development with clean and pragmatic design. Below are some core concepts:

## 1. Model-Template-View (MTV) Architecture
- **Model**: Defines the data structure in the database using Python classes.
- **Template**: Handles the frontend, rendering dynamic HTML pages.
- **View**: Processes requests, interacts with models, and returns responses.

## 2. Django Project vs. Django App
- **Project**: A complete web application framework containing settings and configurations.
- **App**: A modular component within a project that serves a specific functionality.

## 3. URL Routing
- Defined in `urls.py` using `path()` or `re_path()`.
- Maps URLs to view functions or class-based views.
- Example:
  ```python
  from django.urls import path
  from myapp import views

  urlpatterns = [
      path('home/', views.home, name='home'),
  ]
  
## 4. Models and ORM (Object-Relational Mapping)
- Django ORM handles database operations using Python models.


```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
```

Migrations (makemigrations and migrate) update the database schema.

## 5. Views (Function-Based and Class-Based)
- Function-based views (FBV): Handles HTTP requests with simple functions.

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Django!")

Class-based views (CBV): Provides reusable, scalable functionality.

```
## 6. Templates
- Located in the templates/ folder, using Django’s templating engine.


```html
<h1>Welcome, {{ user.name }}</h1>
Includes template tags like {% for item in list %} and {% if condition %}.
```
## 7. Django Admin Panel
- Managed via admin.py and accessed at /admin/.

Registering Models:
```python
from django.contrib import admin
from .models import Book

admin.site.register(Book)
```

## 8. Forms and User Input Handling
- Django Form API (forms.py) simplifies form handling and validation.

```python
from django import forms

class BookForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=100)
```
## 9. Middleware
- Hooks into Django’s request-response cycle to modify behavior.

- Examples: authentication, security, session management.

## 10. Static and Media Files
- **Static files**: CSS, JavaScript stored in /static/.

- **Media files**: User-uploaded files managed via MEDIA_ROOT.

## 11. REST API Development (Django REST Framework)
- Django REST Framework (DRF) helps build APIs.

Example Serializer:
```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```
## 12. Deployment Considerations
- Use Gunicorn or UWSGI with Nginx or Apache.

- Set DEBUG = False in settings.py for production.
