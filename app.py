import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
database_path = Path(__file__).parent / "instance" / "applications.db"
ALLOWED_STATUSES = {
    "Applied",
    "Waiting for Interview",
    "Interviewed",
    "Offer",
    "Rejected",
    "Withdrawn",
}


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
    company = request.form.get("company", "").strip()
    position = request.form.get("position", "").strip()
    wage_text = request.form.get("wage", "").strip()
    status = request.form.get("status", "").strip()

    if not company or not position or not status:
        return "Company, position, and status are required.", 400

    if len(company) > 127:
        return "Company must be 127 characters or fewer.", 400

    if len(position) > 63:
        return "Position must be 63 characters or fewer.", 400

    if status not in ALLOWED_STATUSES:
        return "Invalid application status.", 400

    try:
        wage = float(wage_text) if wage_text else None
    except ValueError:
        return "Wage must be a number.", 400

    if wage is not None and wage < 0:
        return "Wage cannot be negative.", 400

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