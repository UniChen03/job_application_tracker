import unittest

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
            }
        )

        self.assertEqual(
            form_data,
            ("test_comp", "test_posi", 25.0, "Applied"),
        )
        self.assertIsNone(err_msg)

    def test_empty_wage_is_accepted(self):
        form_data, err_msg = validate_application_form(
            {
                "company": "test_comp",
                "position": "test_posi",
                "wage": "",
                "status": "Applied",
            }
        )

        self.assertEqual(
            form_data,
            ("test_comp", "test_posi", None, "Applied"),
        )
        self.assertIsNone(err_msg)


if __name__ == "__main__":
    unittest.main()