import unittest
import json
from app.api.v1.database import DatabaseConnection
from app.api.v1 import app


class LoginTestCase(unittest.TestCase):
    """This tests the login route"""
    def setUp(self):
        self.test_app = app.test_client()
        self.test_db = DatabaseConnection()
        self.table_list = ['users', 'sales', 'products', 'sale_point']

    def tearDown(self):
        for table in self.table_list:
            self.test_db.drop_tables(table)

    def test_admin_login(self):
        self.test_admin_data = {"email_address": "admin@gmail.com",  "password": "admin00"}
        response = self.test_app.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                      data=json.dumps(self.test_admin_data))
        self.assertTrue(response.status_code, 200)
        response_message = json.loads(response.data.decode())
        self.assertIn("You have successfully logged in", response_message["message"])
