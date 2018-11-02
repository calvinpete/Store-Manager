# import unittest
# import json
# from tests.test_baser import TestBase
#
#
# class TestCategoryApi(TestBase):
#     """
#     This is a class that runs unittests on the create category api endpoint
#     """
#     def test_new_category(self):
#         """
#         This tests post create_category method
#         """
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data00), headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 201)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("Foot wear category successfully created", response_message["message"])
#
#     def test_wrong_user(self):
#         """
#         This tests a user without administrator rights
#         """
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data01), headers={'x-access-token': self.token_staff})
#         self.assertEqual(response.status_code, 401)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("You do not have administrator access", response_message["message"])
#
#     def test_invalid_token_create_category(self):
#         """
#         This tests post create_category method with an invalid token
#         """
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data01), headers={'x-access-token': self.token + 'secret'})
#         self.assertEqual(response.status_code, 401)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("Token is invalid", response_message["message"])
#
#     def test_unauthorized_create_category(self):
#         """
#         This tests post create_category method without a token
#         """
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data01))
#         self.assertEqual(response.status_code, 401)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("Token is missing", response_message["message"])
#
#     def test_category_empty_field(self):
#         """
#         This tests create_category post method with no category field
#         """
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data09), headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 400)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("The category field is missing", response_message["message"])
#
#     def test_category_int_type(self):
#         """
#         This tests create_category post method with wrong integer data type in the request
#         """
#         # integer data type
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data02), headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 400)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("Please enter a string", response_message["message"])
#
#     def test_category_float_type(self):
#         """
#         This tests create_category post method with wrong float data type in the request
#         """
#         # float data type
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data03), headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 400)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("Please enter a string", response_message["message"])
#
#     def test_category_list_type(self):
#         """
#         This tests create_category post method with wrong data type in the request
#         """
#         # list data type
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data04), headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 400)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("Please enter a string", response_message["message"])
#
#     def test_no_value_entry(self):
#         """
#         This tests create_category post method with no value in the key/value pair entry
#         """
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data05), headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 400)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("Value for category is required", response_message["message"])
#
#     def test_whitespace_entry(self):
#         """
#         This tests create_category post method with a whitespace invalid entry
#         """
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data07), headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 400)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("Value for category is required", response_message["message"])
#
#     def test_category_exists(self):
#         """
#         This tests create_category post method with a category already created
#         """
#         self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                       data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 409)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("The Spices Category already exists", response_message["message"])
#
#     def test_no_data(self):
#         """
#         This tests create_category post method with no data in the request
#         """
#         response = self.app.post("/store-manager/api/v1/category", content_type="application/json",
#                                  headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 400)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("Invalid entry", response_message["message"])
#
#     def test_wrong_method(self):
#         """
#         This tests a wrong method used for a wrong request
#         """
#         response = self.app.delete("/store-manager/api/v1/category", content_type="application/json",
#                                    data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 405)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("This method is not allowed for the requested URL", response_message["message"])
#
#     def test_page_not_found(self):
#         """
#         This tests a request for a non existent page
#         """
#         response = self.app.post("/job/api/v1/category", content_type="application/json",
#                                  data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
#         self.assertEqual(response.status_code, 404)
#         response_message = json.loads(response.data.decode())
#         self.assertIn("This page does not exist", response_message["message"])
#
#
# if __name__ == "__main__":
#     unittest.main()
