import unittest
import json
from tests.test_baser import TestBase


class TestSalesApi(TestBase):
    """
    This is a class that runs unittests on the sales api endpoints
    """

    def test_create_sale_record(self):
        """
        This tests create sale_record post route
        """
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data081), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Juices/products', content_type="application/json",
                      data=json.dumps(self.test_data30), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data31), headers={'x-access-token': self.token_staff})
        self.assertTrue(response.status_code, 201)
        response_message = json.loads(response.data.decode())
        self.assertIn("Sale record successfully created", response_message["message"])

    def test_wrong_user(self):
        """
        This tests an administrator accessing the route
        """
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data32), headers={'x-access-token': self.token})
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("Only a staff attendant can create a sale record", response_message["message"])

    def test_invalid_token_create_sale_record(self):
        """
        This tests create_sale record with an invalid token
        """
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data32), headers={'x-access-token': self.token_staff + "1"})
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("Token is invalid", response_message["message"])

    def test_unauthorized_create_sale_record(self):
        """
        This tests create_sale record method without a token
        """
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data32))
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("Token is missing", response_message["message"])

    def test_no_entry(self):
        """This tests a create_sale record post method with no field"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data33), headers={'x-access-token': self.token_staff})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("You should have the category, product_id, quantity and sale_type fields",
                      response_message["message"])

    def test_input_int_type(self):
        """This tests a create_sale record post method with an integer as the value in the request"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data34), headers={'x-access-token': self.token_staff})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_input_float_type(self):
        """This tests a create_sale record post method with a float as the value in the request"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data35), headers={'x-access-token': self.token_staff})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_input_list_type(self):
        """This tests a create_sale record post method with a list as the value in the request"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data36), headers={'x-access-token': self.token_staff})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter a string", response_message["message"])

    def test_input_string_type(self):
        """This tests a create_sale record post method with a string as the value in the request"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data08), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data40), headers={'x-access-token': self.token_staff})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter an integer", response_message["message"])

    def test__float_type_parameter(self):
        """This tests a create_sale record post method
        with a float in place of an integer as the value in the request"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data08), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data42), headers={'x-access-token': self.token_staff})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter an integer", response_message["message"])

    def test__list_type_parameter(self):
        """This tests a create_sale record post method with a list in place of an integer as the value in the request"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data08), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data41), headers={'x-access-token': self.token_staff})
        self.assertTrue(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Please enter an integer", response_message["message"])

    def test_no_value_entry(self):
        """This tests a create_sale record post method with no value in the key/value pair entry"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data37), headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Values are required", response_message["message"])

    def test_whitespace_entry(self):
        """This tests a create_sale record post method with a whitespace as an entry in the request"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data38), headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 400)
        response_message = json.loads(response.data.decode())
        self.assertIn("Values are required", response_message["message"])

    def test_exceeded_quantity(self):
        """This tests a create_sale record post method with a quantity more what is in the store"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data08), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                      data=json.dumps(self.test_data12), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data430), headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())
        self.assertIn("Invalid quantity requested", response_message["message"])

    def test_invalid_quantity(self):
        """This tests a create_sale record post method with a quantity more what is in the store"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data08), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Drinks/products', content_type="application/json",
                      data=json.dumps(self.test_data12), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data431), headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())
        self.assertIn("Invalid quantity requested", response_message["message"])

    def test_nonexistent_category(self):
        """This tests a create_sale record post method with a category that does not exist"""
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data320), headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())
        self.assertIn("Lights category does not exist", response_message["message"])

    def test_non_existent_product(self):
        """This tests the create a sale record post route for a non existent product"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data082), headers={'x-access-token': self.token})
        response = self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                                 data=json.dumps(self.test_data321), headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())
        self.assertIn("Product does not exist", response_message["message"])

    def test_get_all_sale_records(self):
        """This tests the fetch all sale_records route"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                      data=json.dumps(self.test_data32), headers={'x-access-token': self.token_staff})
        response = self.app.get('/store-manager/api/v1/sales', content_type="application/json",
                                headers={'x-access-token': self.token})
        self.assertEqual(response.status_code, 200)

    def test_wrong_user_get_all_sale_records(self):
        """This tests the fetch all sale_records route administrative access"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                      data=json.dumps(self.test_data32), headers={'x-access-token': self.token_staff})
        response = self.app.get('/store-manager/api/v1/sales', content_type="application/json",
                                headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 401)
        response_message = json.loads(response.data.decode())
        self.assertIn("You do not have administrator access", response_message["message"])

    def test_get_single_sale_record(self):
        """This tests the get a single sale_record route"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                      data=json.dumps(self.test_data32), headers={'x-access-token': self.token_staff})
        response = self.app.get('/store-manager/api/v1/sales/1', content_type="application/json",
                                headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 200)

    def test_invalid_sale_id(self):
        """This tests the get a single sale_record route with an invalid sale_id"""
        self.app.post("/store-manager/api/v1/category", content_type="application/json",
                      data=json.dumps(self.test_data01), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/Spices/products', content_type="application/json",
                      data=json.dumps(self.test_data26), headers={'x-access-token': self.token})
        self.app.post('/store-manager/api/v1/sales', content_type="application/json",
                      data=json.dumps(self.test_data32), headers={'x-access-token': self.token_staff})
        response = self.app.get('/store-manager/api/v1/sales/-1', content_type="application/json",
                                headers={'x-access-token': self.token_staff})
        self.assertEqual(response.status_code, 404)
        response_message = json.loads(response.data.decode())
        self.assertIn("sale_id should be a positive integer", response_message["message"])


if __name__ == "__main__":
    unittest.main()
