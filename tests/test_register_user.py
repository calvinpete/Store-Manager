import unittest
import json
from app.api.v1.database import DatabaseConnection
from app.api.v1 import app


class SignupTestCase(unittest.TestCase):
    """This tests the signup route"""
    def setUp(self):
        self.test_app = app.test_client()
        self.test_db = DatabaseConnection()
        self.table_list = ['users', 'sales', 'products', 'sale_point']

        self.test_admin_data = {"email_address": "admin@gmail.com",  "password": "admin00"}  # default admin

        #  Administrator logging in to fetch the JSON web token
        admin_response = self.test_app.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                            data=json.dumps(self.test_admin_data))  # admin logging in
        logged_in_user_response = json.loads(admin_response.data.decode())
        self.token = logged_in_user_response["token"]  # admin JSON web token

    def tearDown(self):
        for table in self.table_list:
            self.test_db.drop_tables(table)

    def test_user_register(self):
        self.test_admin_data = {"email_address": "admin@gmail.com",  "password": "admin00"}  # default admin
        admin_response = self.test_app.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                            data=json.dumps(self.test_admin_data))  # admin logging in
        logged_in_response = json.loads(admin_response.data.decode())
        self.token00 = logged_in_response["token"]  # admin JSON web token

        self.test_user_data = {"name": "mark", "email_address": "MK@gmail.com", "password": "Li/x",
                               "account_type": "store_attendant"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_user_data), headers={'x-access-token': self.token00})
        self.assertTrue(response.status_code, 201)
        response_message = json.loads(response.data.decode())
        self.assertIn("mark has been successfully registered", response_message["message"])

    def test_missing_token(self):
        """This holds a test for a signup route that has no JSON web token"""
        self.test_user_data00 = {"name": "clint", "email_address": "hope@gmail.com", "password": "H4!t",
                                 "account_type": "staff_attendant"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_user_data))
        self.assertTrue(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("Token is missing", response_message["message"])

    def test_invalid_token(self):
        """This holds a test for a signup route with an invalid JSON web token"""
        self.test_user_data00 = {"name": "KingDavid", "email_address": "davidking@gmail.com",
                                 "password": "psaLms198?", "account_type": "staff_attendant"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_user_data00),
                                      headers={'x-access-token': self.token + '2'})
        self.assertTrue(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("Token is invalid", response_message["message"])

    def test_wrong_user(self):
        """This tests a user without administrator rights"""

        self.test_register_data = {"name": "Jones", "email_address": "jap@gmail.com", "password": "121",
                                   "account_type": "store_attendant"}

        # Administrator registering Jones a store attendant
        self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                           data=json.dumps(self.test_register_data), headers={'x-access-token': self.token})

        self.test_login_data = {"email_address": "jap@gmail.com", "password": "121"}

        # Jones, the staff attendant logging in to fetch the JSON web token
        staff_response = self.test_app.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                            data=json.dumps(self.test_login_data))  # staff attendant logging in
        logged_in_staff_response = json.loads(staff_response.data.decode())
        self.token_staff = logged_in_staff_response["token"]  # staff attendant JSON web token

        self.test_data00 = {"name": "said", "email_address": "said@gmail.com", "password": "1wq",
                            "account_type": "store_attendant"}

        #  accessing the signup route with Jones' JSON web token
        response = self.test_app.post("/store-manager/api/v1/auth/signup", content_type="application/json",
                                      data=json.dumps(self.test_data00), headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("You do not have administrator access", response_message["message"])

    def test_nonexistent_field(self):
        """This tests the register route with missing fields"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user24), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("please type in the missing fields", response_message["message"])

    def test_no_value(self):
        """This tests the register route with no value in a key value pair"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user25), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Values are required", response_message["message"])

    def test_space_input(self):
        """This tests the register route with a space character as an input"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user26), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Values are required", response_message["message"])

    def test_name_int_data_type(self):
        """This tests the register route with the name as an integer"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user12), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_name_float_data_type(self):
        """This tests the register route with the name as a float"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user13), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_name_list_data_type(self):
        """This tests the register route with the name as a list"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user14), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_email_address_int_data_type(self):
        """This tests the register route with the email_address as an integer"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user15), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_email_address_float_data_type(self):
        """This tests the register route with the email_address as a float"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user16), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_email_address_list_data_type(self):
        """This tests the register route with the email_address as a list"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user17), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_password_int_data_type(self):
        """This tests the register route with the password as an integer"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user18), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_password_float_data_type(self):
        """This tests the register route with the password as a float"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user19), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_password_list_data_type(self):
        """This tests the register route with the password as a list"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user20), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_validate_email_address(self):
        """This tests the register route with an invalid email_address"""
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user21), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("The email should follow the format of valid emails (johndoe@mail.com)",
                      response_message["message"])

    def test_user_already_exists(self):
        """This tests the register route with user credentials already posted"""
        self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                      data=json.dumps(self.test_user29), headers={'x-access-token': self.token})
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user29), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 409)
        response_message = json.loads(response.data.decode())
        self.assertIn("Employee already exists", response_message["message"])