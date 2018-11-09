import unittest
import json
from app.api.v1.database import DatabaseConnection
from app.api.v1 import app
from instance.config import app_config


class LoginTestCase(unittest.TestCase):
    """This tests the login route"""
    def setUp(self):
        app.config.from_object(app_config["testing"])
        self.test_app = app.test_client()
        self.test_db = DatabaseConnection()

    def tearDown(self):
        self.test_db.drop_tables('users')

    def test_admin_login(self):
        self.test_admin_data = {"email_address": "admin@gmail.com",  "password": "admin00"}
        response = self.test_app.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                      data=json.dumps(self.test_admin_data))
        self.assertTrue(response.status_code, 200)
        response_message = json.loads(response.data.decode())
        self.assertIn("You have successfully logged in", response_message["message"])


if __name__ == "__main__":
    unittest.main()
