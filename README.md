# RESTful API for Library Management

This project is part of the CODTECH Software Development Internship (Task 2). It is a Flask-based RESTful API designed to manage a simple library system. It supports CRUD operations and demonstrates clean code structure, endpoint design, and data handling.

---

## Features

-  View all books
-  Add a new book
-  Update existing book details
-  Delete a book
-  Health check endpoint

---

## Endpoints

| Method | Endpoint         | Description                |
|--------|------------------|----------------------------|
| GET    | `/books`         | Get all books              |
| POST   | `/books`         | Add a new book             |
| GET    | `/books/<id>`    | Get a specific book        |
| PUT    | `/books/<id>`    | Update an existing book    |
| DELETE | `/books/<id>`    | Delete a book              |
| GET    | `/health`        | Check API health status    |

---

## How to Run Locally

###  Prerequisites
- Python 3.7+
- Flask

### 📥 Install Dependencies

```bash
pip install -r requirements.txt
