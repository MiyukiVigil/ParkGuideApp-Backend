from django.test import SimpleTestCase


class RangerEyeApiRootTests(SimpleTestCase):
    def test_api_root_is_accessible(self):
        response = self.client.get("/api/ranger-eye/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Ranger Eye API is available.")
        self.assertIn("dashboard_data", response.json()["endpoints"])
