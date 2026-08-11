import unittest
from datetime import date, timedelta

from app import validate_application_form


class ValidateApplicationFormTests(unittest.TestCase):
    def test_required_fields_are_rejected_when_missing(self):
        required_fields = ["company", "position", "status"]

        for field in required_fields:
            with self.subTest(field=field):
                data = {
                    "company": "test_comp",
                    "position": "test_posi",
                    "wage": "25",
                    "status": "Applied",
                }

                data[field] = ""

                form_data, err_msg = validate_application_form(data)

                self.assertIsNone(form_data)
                self.assertEqual(
                    err_msg,
                    "Company, position, and status are required.",
                )

    def test_invalid_application_date_is_rejected(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "test_posi",
                "wage": "25",
                "status": "Applied",
                "application_date": "2026-02-30",
                "notes": "",
            }
        )

        self.assertIsNone(form_data)
        self.assertEqual(
            err_msg,
            "Application date must be a valid date.",
        )

    def test_future_application_date_is_rejected(self):
        future_date = (date.today() + timedelta(days=1)).isoformat()

        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "test_posi",
                "wage": "25",
                "status": "Applied",
                "application_date": future_date,
                "notes": "",
            }
        )

        self.assertIsNone(form_data)
        self.assertEqual(
            err_msg,
            "Application date cannot be in the future.",
        )

    def test_too_long_notes_are_rejected(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "test_posi",
                "wage": "25",
                "status": "Applied",
                "application_date": "2026-08-10",
                "notes": "N" * 2001,
            }
        )

        self.assertIsNone(form_data)
        self.assertEqual(
            err_msg,
            "Notes must be 2000 characters or fewer.",
        )

    def test_invalid_job_urls_are_rejected(self):
        invalid_job_urls = [
            "example.com/job",
            "ftp://example.com/job",
            "https://",
        ]

        for job_url in invalid_job_urls:
            with self.subTest(job_url=job_url):
                form_data, err_msg = validate_application_form(
                    {
                        "company": "test_comp",
                        "position": "test_posi",
                        "wage": "25",
                        "status": "Applied",
                        "application_date": "",
                        "notes": "",
                        "job_url": job_url,
                    }
                )

                self.assertIsNone(form_data)
                self.assertEqual(
                    err_msg,
                    "Job posting URL must be a valid HTTP or HTTPS URL.",
                )

    def test_too_long_job_url_is_rejected(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "test_posi",
                "wage": "25",
                "status": "Applied",
                "application_date": "",
                "notes": "",
                "job_url": "https://example.com/" + "j" * 2030,
            }
        )

        self.assertIsNone(form_data)
        self.assertEqual(
            err_msg,
            "Job posting URL must be 2048 characters or fewer.",
        )

    def test_negative_wage_is_rejected(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "test_posi",
                "wage": "-2",
                "status": "Applied",
            }
        )

        self.assertIsNone(form_data)
        self.assertEqual(
            err_msg,
            "Wage cannot be negative.",
        )

    def test_too_long_company_is_rejected(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "C" * 128,
                "position": "test_posi",
                "wage": "25",
                "status": "Applied",
            }
        )

        self.assertIsNone(form_data)
        self.assertEqual(
            err_msg,
            "Company must be 127 characters or fewer.",
        )

    def test_too_long_position_is_rejected(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "P" * 64,
                "wage": "25",
                "status": "Applied",
            }
        )

        self.assertIsNone(form_data)
        self.assertEqual(
            err_msg,
            "Position must be 63 characters or fewer.",
        )

    def test_invalid_status_is_rejected(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "test_posi",
                "wage": "25",
                "status": "Unknown",
            }
        )

        self.assertIsNone(form_data)
        self.assertEqual(
            err_msg,
            "Invalid application status.",
        )

    def test_non_numeric_wage_is_rejected(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "test_posi",
                "wage": "twenty-five",
                "status": "Applied",
            }
        )

        self.assertIsNone(form_data)
        self.assertEqual(
            err_msg,
            "Wage must be a number.",
        )

    def test_valid_data_is_accepted(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "test_posi",
                "wage": "25",
                "status": "Applied",
                "application_date": "2026-08-10",
                "notes": "  Follow up next week.  ",
                "job_url": "https://example.com/job",
            }
        )

        self.assertEqual(
            form_data,
            (
                "test_comp",
                "test_posi",
                25.0,
                "Applied",
                "2026-08-10",
                "Follow up next week.",
                "https://example.com/job",
            ),
        )
        self.assertIsNone(err_msg)

    def test_empty_wage_is_accepted(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "test_posi",
                "wage": "",
                "status": "Applied",
                "application_date": "",
                "notes": "",
                "job_url": "",
            }
        )

        self.assertEqual(
            form_data,
            (
                "test_comp",
                "test_posi",
                None,
                "Applied",
                None,
                None,
                None,
            ),
        )
        self.assertIsNone(err_msg)


if __name__ == "__main__":
    unittest.main()
