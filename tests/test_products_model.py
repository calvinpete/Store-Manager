# import unittest
# from app.api.v1.models.products import Product
# from tests.test_baser import TestBase
#
#
# class ProductTestCase(TestBase):
#     """
#     This class holds the tests on the products model
#     """
#
#     def test_creation(self):
#         """
#         This tests instance  of the Product class
#         :return:
#         """
#         self.assertIsInstance(self.goods, Product)
#
#     def test_check_category(self):
#         """
#         This tests the check_category method of the Product class
#         :return:
#         """
#         self.assertTrue(self.goods.check_category(self.test_data01["category"]))
#
#     def test_add_product(self):
#         """
#         This tests the add_product method of the Product class
#         :return:
#         """
#         self.assertEqual(len(self.goods.stock.keys()), 1)
#
#     def test_check_product_existence(self):
#         """
#         This tests the check_product_existence method of the Product class
#         :return:
#         """
#         self.assertTrue(
#             self.goods.check_product_existence(
#                 self.test_data01["category"],
#                 self.test_data24["product_name"],
#                 self.test_data24["details"],
#                 self.test_data24["quantity"]
#             )
#         )
#
#     def test_get_single_product(self):
#         """
#         This tests the get_single_product method of the Product class
#         :return:
#         """
#         self.assertEqual(len(self.goods.get_single_product(self.test_data01["category"], 1)), 5)
#
#     def test_get_all_products(self):
#         """
#         This tests the get_all_products method of the Product class
#         :return:
#         """
#         self.assertEqual(len(self.goods.get_all_products()), 1)
#
#
# if __name__ == "__main__":
#     unittest.main()
