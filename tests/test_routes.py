import sqlite3
import tempfile
import unittest
from pathlib import Path

import app as app_module


class ApplicationRouteTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.test_database_path = (
            Path(self.temp_directory.name) / "applications.db"
        )

        schema_path = Path(__file__).parent.parent / "schema.sql"

        connection = sqlite3.connect(self.test_database_path)

        with schema_path.open(encoding="utf-8") as schema_file:
            connection.executescript(schema_file.read())
        connection.close()

        self.original_database_path = app_module.database_path
        app_module.database_path = self.test_database_path

        self.original_testing = app_module.app.config["TESTING"]

        app_module.app.config["TESTING"] = True
        self.client = app_module.app.test_client()

    def test_add_application_saves_valid_data(self):
        response = self.client.post(
            "/applications",
            data={
                "company": "test_comp",
                "position": "test_posi",
                "wage": "25.00",
                "status": "Applied",
            },
        )

        self.assertEqual(response.status_code, 302)

        connection = sqlite3.connect(self.test_database_path)
        application = connection.execute(
            """
            SELECT company, position, wage, status
            FROM applications
            """
        ).fetchone()
        connection.close()

        self.assertEqual(
            application,
            ("test_comp", "test_posi", 25.00, "Applied"),
        )

    def test_add_application_rejects_invalid_data(self):
        response = self.client.post(
            "/applications",
            data={
                "company": "",
                "position": "test_posi",
                "wage": "25.00",
                "status": "Applied",
            },
        )

        self.assertEqual(response.status_code, 400)

        connection = sqlite3.connect(self.test_database_path)
        row_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM applications
            """
        ).fetchone()[0]
        connection.close()

        self.assertEqual(row_count, 0)

    def test_index_displays_saved_application(self):
        connection = sqlite3.connect(self.test_database_path)
        connection.execute(
            """
            INSERT INTO applications (company, position, wage, status)
            VALUES (?, ?, ?, ?)
            """,
            ("test_comp", "test_posi", 30.00, "Applied"),
        )
        connection.commit()
        connection.close()

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        page_html = response.get_data(as_text=True)

        self.assertIn("test_comp", page_html)
        self.assertIn("test_posi", page_html)
        self.assertIn("$30.00", page_html)

    def test_edit_application_updates_existing_data(self):
        connection = sqlite3.connect(self.test_database_path)
        cursor = connection.execute(
            """
            INSERT INTO applications (company, position, wage, status)
            VALUES (?, ?, ?, ?)
            """,
            ("test_comp", "test_posi", 30.00, "Applied"),
        )
        application_id = cursor.lastrowid
        connection.commit()
        connection.close()

        response = self.client.post(
            f"/applications/{application_id}/edit",
            data={
                "company": "new_test_comp",
                "position": "new_test_posi",
                "wage": "25.00",
                "status": "Rejected",
            },
        )

        self.assertEqual(response.status_code, 302)

        connection = sqlite3.connect(self.test_database_path)
        application = connection.execute(
            """
            SELECT company, position, wage, status
            FROM applications
            WHERE id = ?
            """,
            (application_id,),
        ).fetchone()
        connection.close()

        self.assertEqual(
            application,
            ("new_test_comp", "new_test_posi", 25.00, "Rejected"),
        )

    def test_edit_nonexistent_application_returns_404(self):
        response = self.client.post(
            "/applications/999/edit",
            data={
                "company": "test_comp",
                "position": "test_posi",
                "wage": "25.00",
                "status": "Applied",
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn(
            "Application not found.",
            response.get_data(as_text=True),
        )

    def test_delete_application_deletes_existing_application(self):
        connection = sqlite3.connect(self.test_database_path)
        cursor = connection.execute(
            """
            INSERT INTO applications (company, position, wage, status)
            VALUES (?, ?, ?, ?)
            """,
            ("test_comp", "test_posi", 30.00, "Applied"),
        )
        application_id = cursor.lastrowid
        connection.commit()
        connection.close()

        response = self.client.post(
            f"/applications/{application_id}/delete",
        )

        self.assertEqual(response.status_code, 302)

        connection = sqlite3.connect(self.test_database_path)
        row_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM applications
            WHERE id = ?
            """,
            (application_id,),
        ).fetchone()[0]
        connection.close()

        self.assertEqual(row_count, 0)

    def test_delete_nonexistent_application_returns_404(self):
        response = self.client.post(
            "/applications/999/delete",
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn(
            "Application not found.",
            response.get_data(as_text=True),
        )

    def test_index_displays_empty_state(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "No applications yet. Add one using the form above.",
            response.get_data(as_text=True),
        )

    def test_index_filters_applications_by_status(self):
        connection = sqlite3.connect(self.test_database_path)
        connection.executemany(
            """
            INSERT INTO applications (company, position, wage, status)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("test_applied_comp", "test_posi", 25.00, "Applied"),
                ("test_rejected_comp", "test_posi", 30.00, "Rejected"),
            ],
        )
        connection.commit()
        connection.close()

        response = self.client.get("/?status=Applied")

        self.assertEqual(response.status_code, 200)

        page_html = response.get_data(as_text=True)

        self.assertIn("test_applied_comp", page_html)
        self.assertNotIn("test_rejected_comp", page_html)

    def test_index_displays_no_filter_matches_message(self):
        connection = sqlite3.connect(self.test_database_path)
        connection.execute(
            """
            INSERT INTO applications (company, position, wage, status)
            VALUES (?, ?, ?, ?)
            """,
            ("test_applied_comp", "test_posi", 25.00, "Applied"),
        )
        connection.commit()
        connection.close()

        response = self.client.get("/?status=Rejected")

        self.assertEqual(response.status_code, 200)

        page_html = response.get_data(as_text=True)

        self.assertIn(
            "No applications match the Rejected status.",
            page_html,
        )
        self.assertNotIn(
            "No applications yet. Add one using the form above.",
            page_html,
        )

    def test_index_rejects_invalid_status_filter(self):
        response = self.client.get("/?status=invalid_status")

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Invalid application status.",
            response.get_data(as_text=True),
        )

    def test_index_searches_by_company_or_position(self):
        connection = sqlite3.connect(self.test_database_path)
        connection.executemany(
            """
            INSERT INTO applications (company, position, wage, status)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("Python Industries", "Accountant", 25.0, "Applied"),
                ("Code Company", "Python Developer", 30.0, "Applied"),
                ("Design Company", "Designer", 35.0, "Applied"),
            ],
        )
        connection.commit()
        connection.close()

        response = self.client.get("/?search=python")

        self.assertEqual(response.status_code, 200)

        page_html = response.get_data(as_text=True)

        self.assertIn("Python Industries", page_html)
        self.assertIn("Code Company", page_html)
        self.assertNotIn("Design Company", page_html)

    def test_index_displays_no_keyword_matches_message(self):
        connection = sqlite3.connect(self.test_database_path)
        connection.execute(
            """
            INSERT INTO applications (company, position, wage, status)
            VALUES (?, ?, ?, ?)
            """,
            ("test_comp", "test_posi", 25.00, "Applied"),
        )
        connection.commit()
        connection.close()

        response = self.client.get("/?search=invalid_keyword")

        self.assertEqual(response.status_code, 200)

        page_html = response.get_data(as_text=True)

        self.assertIn(
            "No applications match the keyword \"invalid_keyword\".",
            page_html,
        )
        self.assertNotIn(
            "No applications yet. Add one using the form above.",
            page_html,
        )

    def test_index_combines_status_filter_and_search(self):
        connection = sqlite3.connect(self.test_database_path)
        connection.executemany(
            """
            INSERT INTO applications (company, position, wage, status)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("Applied Python Company", "Developer", 25.0, "Applied"),
                ("Rejected Python Company", "Developer", 30.0, "Rejected"),
                ("Applied Design Company", "Designer", 35.0, "Applied"),
            ],
        )
        connection.commit()
        connection.close()

        response = self.client.get(
            "/?status=Applied&search=python"
        )

        self.assertEqual(response.status_code, 200)

        page_html = response.get_data(as_text=True)

        self.assertIn("Applied Python Company", page_html)
        self.assertNotIn("Rejected Python Company", page_html)
        self.assertNotIn("Applied Design Company", page_html)

    def test_index_sorts_applications(self):
        connection = sqlite3.connect(self.test_database_path)
        connection.executemany(
            """
            INSERT INTO applications (company, position, wage, status)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("Zulu Company", "Alpha Position", 20.0, "Applied"),
                ("Alpha Company", "Zulu Position", 40.0, "Applied"),
            ],
        )
        connection.commit()
        connection.close()

        sort_cases = [
            ("newest", "Alpha Company", "Zulu Company"),
            ("company", "Alpha Company", "Zulu Company"),
            ("position", "Zulu Company", "Alpha Company"),
            ("wage", "Alpha Company", "Zulu Company"),
        ]

        for sort_option, first_company, second_company in sort_cases:
            with self.subTest(sort_option=sort_option):
                response = self.client.get(f"/?sort={sort_option}")

                self.assertEqual(response.status_code, 200)

                page_html = response.get_data(as_text=True)

                first_position = page_html.index(first_company)
                second_position = page_html.index(second_company)

                self.assertLess(first_position, second_position)

    def test_index_rejects_invalid_sort_option(self):
        response = self.client.get("/?sort=invalid_sort")

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Invalid sort option.",
            response.get_data(as_text=True),
        )

    def tearDown(self):
        app_module.database_path = self.original_database_path
        app_module.app.config["TESTING"] = self.original_testing
        self.temp_directory.cleanup()