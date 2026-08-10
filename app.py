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
    "Other",
}
SORT_OPTIONS = {
    "newest": "id DESC",
    "company": "company COLLATE NOCASE ASC",
    "position": "position COLLATE NOCASE ASC",
    "wage": "wage DESC",
}


def get_db_connection():
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def validate_application_form(form):
    company = form.get("company", "").strip()
    position = form.get("position", "").strip()
    wage_text = form.get("wage", "").strip()
    status = form.get("status", "").strip()

    if not company or not position or not status:
        return None, "Company, position, and status are required."

    if len(company) > 127:
        return None, "Company must be 127 characters or fewer."

    if len(position) > 63:
        return None, "Position must be 63 characters or fewer."

    if status not in ALLOWED_STATUSES:
        return None, "Invalid application status."

    try:
        wage = float(wage_text) if wage_text else None
    except ValueError:
        return None, "Wage must be a number."

    if wage is not None and wage < 0:
        return None, "Wage cannot be negative."

    return (company, position, wage, status), None


@app.route("/")
def index():
    page_title = "Job Application Tracker"
    selected_status = request.args.get("status", "").strip()
    search_keyword = request.args.get("search", "").strip()
    selected_sort = (request.args.get("sort", "newest").strip() or "newest")

    if selected_status and selected_status not in ALLOWED_STATUSES:
        return "Invalid application status.", 400

    if selected_sort not in SORT_OPTIONS:
        return "Invalid sort option.", 400

    connection = get_db_connection()

    query = """
            SELECT id, company, position, wage, status
            FROM applications
    """
    conditions = []
    parameters = []

    if selected_status:
        conditions.append("status = ?")
        parameters.append(selected_status)

    if search_keyword:
        search_pattern = f"%{search_keyword.lower()}%"

        conditions.append(
            "(LOWER(company) LIKE ? OR LOWER(position) LIKE ?)"
        )
        parameters.extend([search_pattern, search_pattern])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += f" ORDER BY {SORT_OPTIONS[selected_sort]}"

    applications = connection.execute(
        query,
        tuple(parameters),
    ).fetchall()
    connection.close()

    return render_template(
        "index.html",
        page_title=page_title,
        applications=applications,
        selected_status=selected_status,
        status_options=sorted(ALLOWED_STATUSES),
        search_keyword=search_keyword,
        selected_sort=selected_sort,
    )


@app.route("/applications", methods=["POST"])
def add_application():
    form_data, err_msg = validate_application_form(request.form)

    if err_msg is not None:
        return err_msg, 400

    company, position, wage, status = form_data

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


@app.route("/applications/<int:application_id>/delete", methods=["GET", "POST"])
def delete_application(application_id):
    connection = get_db_connection()

    application = connection.execute(
        """
        SELECT id, company, position
        FROM applications
        WHERE id = ?
        """,
        (application_id,),
    ).fetchone()
    connection.close()

    if application is None:
        return "Application not found.", 404

    if request.method == "POST":
        connection = get_db_connection()
        connection.execute(
            """
            DELETE FROM applications
            WHERE id = ?
            """,
            (application_id,),
        )
        connection.commit()
        connection.close()

        return redirect(url_for("index"))

    return render_template(
        "delete.html",
        application=application,
    )


@app.route("/applications/<int:application_id>/edit", methods=["GET", "POST"])
def edit_application(application_id):
    connection = get_db_connection()

    application = connection.execute(
        """
        SELECT id, company, position, wage, status
        FROM applications
        WHERE id = ?
        """,
        (application_id,),
    ).fetchone()
    connection.close()

    if application is None:
        return "Application not found.", 404

    if request.method == "POST":
        form_data, err_msg = validate_application_form(request.form)

        if err_msg is not None:
            return err_msg, 400

        company, position, wage, status = form_data

        connection = get_db_connection()
        connection.execute(
            """
            UPDATE applications
            SET company = ?, position = ?, wage = ?, status = ?
            WHERE id = ?
            """,
            (company, position, wage, status, application_id),
        )
        connection.commit()
        connection.close()

        return redirect(url_for("index"))

    return render_template(
        "edit.html",
        application=application,
    )