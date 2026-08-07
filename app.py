import sqlite3
from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)
database_path = Path(__file__).parent / "instance" / "applications.db"


def get_db_connection():
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def index():
    page_title = "Job Application Tracker"

    connection = get_db_connection()
    applications = connection.execute(
        """
        SELECT id, company, position, wage, status
        FROM applications
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        page_title=page_title,
        applications=applications,
    )