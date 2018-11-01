import unittest
import json
from tests.test_baser import TestBase


class TestProductApi(TestBase):
    """
    This is a class that runs unittests on the product api endpoints
    """

    def test_add_product(self):
        """
        This tests add a product route
        """
        response = self.app.post('/store-manager/api/v1/products', content_type="application/json",
                                 data=json.dumps(self.test_data30), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 201)
        response_message = json.loads(response.data.decode())
        self.assertIn("Product successfully added", response_message["message"])

    def test_existent_product(self):
        """
        This tests add a product route with an already existing product
        """
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data27), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                                 data=json.dumps(self.test_data27), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 200)
        response_message = json.loads(response.data.decode())
        self.assertIn("100ml Western Coriander's quantity has been updated", response_message["message"])

    def test_wrong_user(self):
        """
        This tests a user without administrator rights
        """
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data08), headers={'x-access-token': self.token})
        response = self.app.post("/store-manager/api/v1/Drinks/products", content_type="application/json",
                                 data=json.dumps(self.test_data29), headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("You do not have administrator access", response_message["message"])

    def test_invalid_token_add_product(self):
        """
        This tests add_product method with an invalid token
        """
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                                 data=json.dumps(self.test_data29), headers={'x-access-token': self.token + 'secret'})
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("Token is invalid", response_message["message"])

    def test_unauthorized_add_product(self):
        """
        This tests add_product method without a token
        """
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                                 data=json.dumps(self.test_data29))
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("Token is missing", response_message["message"])

    def test_no_entry(self):
        """This tests a add_product post method with no field"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        response = self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                                 data=json.dumps(self.test_data300), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("You should have the product_name, quantity, details and price fields",
                      response_message["message"])

    def test_input_int_type(self):
        """This tests a add_product post method with an integer as the value in the request"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        response = self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                                 data=json.dumps(self.test_data14), headers={"x-access-token": self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_input_float_type(self):
        """This tests a add_product post method with a float as the value in the request"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        response = self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                                 data=json.dumps(self.test_data15), headers={"x-access-token": self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_input_list_type(self):
        """This tests a add_product post method with a list as the value in the request"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        response = self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                                 data=json.dumps(self.test_data16), headers={"x-access-token": self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_input_string_type(self):
        """This tests a add_product post method with a string as the value in the request"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        response = self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                                 data=json.dumps(self.test_data20), headers={"x-access-token": self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter an integer", response_message["message"])

    def test__float_type_parameter(self):
        """This tests a add_product post method with a float in place of an integer as the value in the request"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        response = self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                                 data=json.dumps(self.test_data22), headers={"x-access-token": self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter an integer", response_message["message"])

    def test__list_type_parameter(self):
        """This tests a add_product post method with a list in place of an integer as the value in the request"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        response = self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                                 data=json.dumps(self.test_data21), headers={"x-access-token": self.token})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter an integer", response_message["message"])

    def test_no_value_entry(self):
        """This tests a add_product post method with no value in the key/value pair entry"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        response = self.app.post("/store-manager/api/v1/Drinks/products", content_type="application/json",
                                 data=json.dumps(self.test_data17), headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Values are required", response_message["message"])

    def test_whitespace_entry(self):
        """This tests a add_product post method with a whitespace as an entry in the request"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        response = self.app.post("/store-manager/api/v1/Drinks/products", content_type="application/json",
                                 data=json.dumps(self.test_data18), headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Values are required", response_message["message"])

    def test_nonexistent_category(self):
        """This tests a add_product post method with a category that does not exist"""
        response = self.app.post("/store-manager/api/v1/camp/products", content_type="application/json",
                                 data=json.dumps(self.test_data28), headers={"x-access-token": self.token})
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())
        self.assertIn("camp category does not exist", response_message["message"])

    def test_get_all_products(self):
        """This tests the get all products get route"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        self.app.post("/store-manager/api/v1/Drinks/products", content_type="application/json",
                      data=json.dumps(self.test_data24), headers={"x-access-token": self.token})
        response = self.app.get("/store-manager/api/v1/products", content_type="application/json",
                                headers={"x-access-token": self.token_staff})
        self.assertEqual(response.status_code, 200)

    def test_get_single_products(self):
        """This tests the get a single product route"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        self.app.post("/store-manager/api/v1/Drinks/products", content_type="application/json",
                      data=json.dumps(self.test_data19), headers={"x-access-token": self.token})
        response = self.app.get("/store-manager/api/v1/Drinks/products/1", content_type="application/json",
                                headers={"x-access-token": self.token_staff})
        self.assertEqual(response.status_code, 200)

    def test_invalid_product_id(self):
        """This tests the get a single product route with an invalid product id"""
        self.app.post("/store-manager/api/v1/products", content_type="application/json",
                      data=json.dumps(self.test_data08))
        self.app.post("/store-manager/api/v1/Drinks/products", content_type="application/json",
                      data=json.dumps(self.test_data26), headers={"x-access-token": self.token})
        response = self.app.get("/store-manager/api/v1/Drinks/products/-4", content_type="application/json",
                                headers={"x-access-token": self.token_staff})
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())
        self.assertIn("Product_id should be a positive integer", response_message["message"])

    def test_non_existent_category(self):
        """This tests the get a single product route with from a non existent category"""
        response = self.app.get("/store-manager/api/v1/Blog/products/1", content_type="application/json",
                                headers={"x-access-token": self.token_staff})
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())
        self.assertIn("Blog category does not exist", response_message["message"])

    def test_non_existent_product(self):
        """This tests the get a single product route for a non existent product"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data082), headers={"x-access-token": self.token})
        response = self.app.get("/store-manager/api/v1/Detergents/products/1", content_type="application/json",
                                headers={"x-access-token": self.token_staff})
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())
        self.assertIn("Product does not exist", response_message["message"])


if __name__ == "__main__":
    unittest.main()
