# import unittest
# from app.api.v1.models.sales import Sales
# from tests.test_baser import TestBase
#
#
# class SalesTestCase(TestBase):
#     """
#     This class holds the tests on the sales model
#     """
#
#     def test_creation(self):
#         """
#         This tests instance of the Sales class
#         :return:
#         """
#         self.assertIsInstance(self.sample_sales, Sales)
#
#     def test_new_sale_record(self):
#         """
#         This tests the sale_product method of the Sales class
#         when the first sale record is created by a store attendant
#         :return:
#         """
#         self.assertEqual(len(self.sample_sales.sales_records.keys()), 1)
#
#     def test_another_sale_record(self):
#         """
#         This tests the sale_product method of the Sales class
#         when a second sale record is created by the same store attendant
#         :return:
#         """
#         all_sale_records = self.sample_sales.sale_product("Drinks", 1, 1, "cash", self.store_attendant)
#         record_by_sale_attendant = all_sale_records.get(self.store_attendant)
#         self.assertEqual(len(record_by_sale_attendant), 2)
#
#     def test_get_sale_record(self):
#         """
#         This tests the get sale record method of the Sales class
#         :return:
#         """
#         self.assertEqual(len(self.sample_sales.get_sale_record(self.store_attendant, 1).keys()), 9)
#
#     def test_get_all_sale_records(self):
#         """
#         This tests the get_all_sale_records method of the Sales class
#         :return:
#         """
#         self.assertEqual(len(self.sample_sales.get_all_sales()), 1)
#
#
# if __name__ == "__main__":
#     unittest.main()
