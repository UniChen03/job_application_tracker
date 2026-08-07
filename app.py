import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

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


@app.route("/applications", methods=["POST"])
def add_application():
    company = request.form["company"]
    position = request.form["position"]
    wage_text = request.form["wage"]
    status = request.form["status"]

    wage = float(wage_text) if wage_text else None

    connection = get_db_connection()
    connection.execute(
        """
        INSERT INTO applications (company, position, wage, status)
        VALUES (?, ?, ?, ?)
        """,
        (company, position, wage, status),
    )

    connection.commit()
    connection.close()

    return redirect(url_for("index"))