# Job Application Tracker

A learning-focused Flask web application for tracking job applications through different stages of the application process.

## Features

- Create job applications
- View applications stored in SQLite
- Edit applications inline
- Delete applications with a confirmation dialog
- Filter applications by status
- Validate application data on the server
- Display wages in US dollar format
- Test validation and CRUD routes with Python unittest
- Search applications by company or position
- Sort applications by date added, application date, company, position, or wage
- View total and status-based application counts
- Track an optional application date and notes
- Save an optional link to the original job posting

## Technology Stack

- Python
- Flask
- SQLite using Python's built-in sqlite3 module
- Jinja HTML templates
- HTML and CSS
- Vanilla JavaScript
- Python unittest

## Run Locally

These instructions use Windows PowerShell.

1. Clone the repository:

    ```powershell
    git clone https://github.com/UniChen03/job_application_tracker.git
    cd job_application_tracker
    ```

2. Create a virtual environment:

    ```powershell
    python -m venv .venv
    ```

3. Install the dependencies:

    ```powershell
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    ```

4. Initialize the database:

    ```powershell
    .\.venv\Scripts\python.exe .\init_db.py
    ```

5. Start the development server:

    ```powershell
    .\.venv\Scripts\python.exe -m flask --app app run --debug
    ```

6. Open `http://127.0.0.1:5000` in a browser.

## Run Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test*.py" -v
```

The tests use temporary SQLite databases and do not modify the real application database.

## Project Purpose

This project was built to learn Flask routing, HTML forms, Jinja templates, SQLite, CRUD operations, server-side validation, Git, and automated testing.
