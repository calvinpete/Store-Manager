import unittest
import json
from tests.test_baser import TestBase


class RegisterRoutesTestCase(TestBase):
    """
    This class holds the unittests on the staff attendant register API endpoints
    """
    def test_register(self):
        """This tests the register route"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user29), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 201)
        response_message = json.loads(response.data.decode())
        self.assertIn("Employee successfully registered", response_message["message"])

    def test_invalid_token_register(self):
        """
        This tests the register route with an invalid token
        """
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_data29), headers={'x-access-token': self.token + 'secret'})
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("Token is invalid", response_message["message"])

    def test_unauthorized_register(self):
        """
        This tests the register route without a token
        """
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_data29))
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("Token is missing", response_message["message"])

    def test_nonexistent_field(self):
        """This tests the register route with missing fields"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user24), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("please type in the missing fields", response_message["message"])

    def test_no_value(self):
        """This tests the register route with no value in a key value pair"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user25), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Values are required", response_message["message"])

    def test_space_input(self):
        """This tests the register route with a space character as an input"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user26), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Values are required", response_message["message"])

    def test_name_int_data_type(self):
        """This tests the register route with the name as an integer"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user12), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_name_float_data_type(self):
        """This tests the register route with the name as a float"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user13), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_name_list_data_type(self):
        """This tests the register route with the name as a list"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user14), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_email_address_int_data_type(self):
        """This tests the register route with the email_address as an integer"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user15), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_email_address_float_data_type(self):
        """This tests the register route with the email_address as a float"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user16), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_email_address_list_data_type(self):
        """This tests the register route with the email_address as a list"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user17), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_password_int_data_type(self):
        """This tests the register route with the password as an integer"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user18), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_password_float_data_type(self):
        """This tests the register route with the password as a float"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user19), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_password_list_data_type(self):
        """This tests the register route with the password as a list"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user20), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_validate_email_address(self):
        """This tests the register route with an invalid email_address"""
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user21), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("The email should follow the format of valid emails (johndoe@mail.com)",
                      response_message["message"])

    def test_user_already_exists(self):
        """This tests the register route with user credentials already posted"""
        self.app.post('/store-manager/api/v1/register', content_type="application/json",
                      data=json.dumps(self.test_user29), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/register', content_type="application/json",
                                 data=json.dumps(self.test_user29), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 409)
        response_message = json.loads(response.data.decode())
        self.assertIn("Employee already exists", response_message["message"])


if __name__ == "__main__":
    unittest.main()
