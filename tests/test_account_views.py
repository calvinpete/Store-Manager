import unittest
import json
import jwt
from instance.config import Config
from tests.test_baser import TestBase


class AccountRoutesTestCase(TestBase):
    """
    This class holds the unittests on the login and signup API endpoints
    """
    def test_signup(self):
        """This tests the signup route"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user1))
        self.assertTrue(response.status_code, 201)
        response_message = json.loads(response.data.decode())
        self.assertIn("You've been successfully registered", response_message["message"])

    def test_nonexistent_field(self):
        """This tests a post method with missing fields"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user24))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("please type in the missing fields", response_message["message"])

    def test_no_value(self):
        """This tests a post method no value in a key value pair"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user25))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Values are required", response_message["message"])

    def test_space_input(self):
        """This tests a post method a space character as an input"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user26))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Values are required", response_message["message"])

    def test_name_int_data_type(self):
        """This tests a post method with username in as an integer"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user12))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_name_float_data_type(self):
        """This tests a post method with username in as a float"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user13))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_name_list_data_type(self):
        """This tests a post method with username in as a list"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user14))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_email_address_int_data_type(self):
        """This tests a post method with email_address in as an integer"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user15))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_email_address_float_data_type(self):
        """This tests a post method with email_address in as a float"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user16))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_email_address_list_data_type(self):
        """This tests a post method with email_address in as a list"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user17))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_password_int_data_type(self):
        """This tests a post method with password in as an integer"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user18))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_password_float_data_type(self):
        """This tests a post method with password in as a float"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user19))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_password_list_data_type(self):
        """This tests a post method with password in as a list"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user20))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_validate_email_address(self):
        """This tests a post method with an invalid email_address"""
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user21))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("The email should follow the format of valid emails (johndoe@mail.com)",
                      response_message["message"])

    def test_user_already_exists(self):
        """This tests a post method with user credentials already posted"""
        self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                      data=json.dumps(self.test_user1))
        response = self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                 data=json.dumps(self.test_user1))
        self.assertTrue(response.status_code, 409)
        response_message = json.loads(response.data.decode())
        self.assertIn("User already exists", response_message["message"])

    def test_login_missing_fields(self):
        """This tests a post method with missing fields"""
        response = self.app.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                 data=json.dumps(self.test_user28))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("please type in the missing fields", response_message["message"])

    def test_login(self):
        """This tests the login route"""
        self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                      data=json.dumps(self.test_user22))
        response = self.app.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                 data=json.dumps(self.test_user221))
        self.assertTrue(response.status_code, 200)
        response_message = json.loads(response.data.decode())
        self.assertIn("You have successfully logged in", response_message["message"])
        data = jwt.decode(response_message["token"], Config.SECRET_KEY)
        self.assertEqual(self.test_user221["email_address"], data["email_address"])

    def test_nonexistent_user(self):
        """This tests a login post method with an unregistered user"""
        response = self.app.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                 data=json.dumps(self.test_user271))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("User does not exist, please register", response_message["message"])

    def test_incorrect_login_password(self):
        """This tests a login post method with an incorrect password"""
        self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                      data=json.dumps(self.test_user23))
        response = self.app.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                 data=json.dumps(self.test_user231))
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Invalid password, please try again", response_message["message"])


if __name__ == "__main__":
    unittest.main()
