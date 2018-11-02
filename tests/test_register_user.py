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
        """This tests the signup route"""
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
        """This tests for a signup route without some fields"""
        self.test_data01 = {"name": "poker", "email_address": "aqpq@gmail.com"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("please make sure you have the name, email_address, password "
                      "and account_type fields only!", response_message["message"])

    def test_no_name_value(self):
        """This tests for a signup route with no value of name in the key value pair"""
        self.test_data02 = {"name": "", "email_address": "egrg@gmail.com", "password": "hse",
                            "account_type": "store_attendant"}

        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data02), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of name is missing", response_message["message"])

    def test_no_email_address_value(self):
        """This tests for a signup route with no value of the email_address in the key value pair"""
        self.test_data03 = {"name": "shakira", "email_address": "", "password": "Kpl",
                            "account_type": "store_attendant"}

        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data03), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of email_address is missing", response_message["message"])

    def test_no_password_value(self):
        """This tests for a signup route with no value of the password key"""
        self.test_data04 = {"name": "sr3rc2", "email_address": "has@gmail.com", "password": "",
                            "account_type": "store_attendant"}

        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data04), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of password is missing", response_message["message"])

    def test_no_account_type_value(self):
        """This tests for a signup route with no value of the account_type key"""
        self.test_data041 = {"name": "sr3rc2", "email_address": "has@gmail.com", "password": "",
                             "account_type": ""}

        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data041), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the account_type value is missing", response_message["message"])

    def test_space_input_name(self):
        """This tests the signup route with a space character in the name value as an input"""
        self.test_data05 = {"name": "  ", "email_address": "wq2@gmail.com", "password": "1q1k0s",
                            "account_type": "store_attendant"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data05), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of name is missing", response_message["message"])

    def test_space_input_email(self):
        """This tests the signup route with a space character in the name email_address as an input"""
        self.test_data06 = {"name": "LMZ", "email_address": "     ", "password": "q23",
                            "account_type": "store_attendant"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data06), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of email_address is missing", response_message["message"])

    def test_space_input_password(self):
        """This tests the signup route with a space character in the password value as an input"""
        self.test_data07 = {"name": "predy", "email_address": "eqpwx@gmail.com", "password": "  ",
                            "account_type": "store_attendant"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data07), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of password is missing", response_message["message"])

    def test_space_input_account_type(self):
        """This tests the signup route with a space character in the account_type value as an input"""
        self.test_data08 = {"name": "Destra", "email_address": "trap6e@gmail.com", "password": "cal2l2x",
                            "account_type": "  "}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data08), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the account_type value is missing", response_message["message"])

    def test_name_int_data_type(self):
        """This tests the signup route with the value of name as an integer"""
        self.test_data09 = {"name": 23, "email_address": "J20ed@gmail.com", "password": "4rd2-",
                            "account_type": "admin"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data09), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of name should be a string", response_message["message"])

    def test_name_float_data_type(self):
        """This tests the signup route with the value of name as a float"""
        self.test_data10 = {"name": 23.999, "email_address": "maks2w@gmail.com", "password": "2-",
                            "account_type": "admin"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data10), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of name should be a string", response_message["message"])

    def test_name_list_data_type(self):
        """This tests the signup route with the value of name as a list"""
        self.test_data11 = {"name": [23.999], "email_address": "qwcw@gmail.com", "password": "2-cqcc",
                            "account_type": "admin"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data11), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of name should be a string", response_message["message"])

    def test_email_address_int_data_type(self):
        """This tests the signup route with the value of the email_address as an integer"""
        self.test_data12 = {"name": "lamar", "email_address": 9, "password": "2-cqcc", "account_type": "admin"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data12), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of email_address should be a string", response_message["message"])

    def test_email_address_float_data_type(self):
        """This tests the signup route with the value of the email_address as a float"""
        self.test_data13 = {"name": "DW", "email_address": 1.2, "password": "float", "account_type": "store_attendant"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data13), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of email_address should be a string", response_message["message"])

    def test_email_address_list_data_type(self):
        """This tests the signup route with the value of the email_address key as a list"""
        self.test_data14 = {"name": "xwd21", "email_address": [23.999], "password": "2", "account_type": "admin"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data14), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of email_address should be a string", response_message["message"])

    def test_password_int_data_type(self):
        """This tests the signup route with the value of the password key as an integer"""
        self.test_data15 = {"name": "211", "email_address": "thqs @gmail.com", "password": 9,
                            "account_type": "admin"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data15), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of password should be a string", response_message["message"])

    def test_password_float_data_type(self):
        """This tests the signup route with the value of the password key as a float"""
        self.test_data16 = {"name": "qewfv", "email_address": "uyj@gmail.com", "password": 2.9,
                            "account_type": "admin"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data16), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of password should be a string", response_message["message"])

    def test_password_list_data_type(self):
        """This tests the signup route with the value of the password key as a list"""
        self.test_data17 = {"name": "t34", "email_address": "tq23h4@gmail.com", "password": ["ss"],
                            "account_type": "admin"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data17), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the value of password should be a string", response_message["message"])

    def test_account_type_int_data_type(self):
        """This tests the signup route with the value of the account_type key as an integer"""
        self.test_data18 = {"name": "211", "email_address": "thqs @gmail.com", "password": "admin",
                            "account_type": 2}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data18), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the account_type value should be a string", response_message["message"])

    def test_account_type_float_data_type(self):
        """This tests the signup route with the value of the account_type key as a float"""
        self.test_data19 = {"name": "qewfv", "email_address": "uyj@gmail.com", "password": "admin",
                            "account_type": 2.9}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data19), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the account_type value should be a string", response_message["message"])

    def test_account_type_list_data_type(self):
        """This tests the signup route with the value of the account_type key as a list"""
        self.test_data20 = {"name": "t34", "email_address": "tq23h4@gmail.com", "password": "admin",
                            "account_type": ["ss"]}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data20), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please note that the account_type value should be a string", response_message["message"])

    def test_validate_email_address(self):
        """This tests the signup route with an invalid email_address"""
        self.test_data21 = {"name": "t3frcf", "email_address": "5u.gmail.com", "password": "wqc",
                            "account_type": "store_attendant"}
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data18), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("The email should follow the format of valid emails (johndoe@mail.com)",
                      response_message["message"])

    def test_user_already_exists(self):
        """This tests the signup route with user credentials already posted"""
        self.test_data22 = {"name": "calvin", "email_address": "Cn@gmail.com", "password": "cv",
                            "account_type": "store_attendant"}
        self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                           data=json.dumps(self.test_data22), headers={'x-access-token': self.token})
        response = self.test_app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                      data=json.dumps(self.test_data22), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 409)
        response_message = json.loads(response.data.decode())
        self.assertIn("calvin is already registered", response_message["message"])
