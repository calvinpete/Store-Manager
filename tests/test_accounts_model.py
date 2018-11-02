# import unittest
# from app.api.v1.models.accounts import Account
# from tests.test_baser import TestBase
#
#
# class AccountTestCase(TestBase):
#     """This class holds the tests on the accounts model"""
#
#     def test_creation(self):
#         """
#         This method tests instance of a class
#         :return:
#         """
#         self.assertIsInstance(self.user_account, Account)

#     def test_register(self):
#         """
#         This method tests the register method of the Account class
#         :return:
#         """
#         self.assertEqual(len(
#             self.user_account.register(
#                 self.test_user1["name"], self.test_user1["email_address"], self.test_user1["password"]
#             )), 2)
#
#     def test_check_user(self):
#         """
#         This method tests the check_user method of the Account class
#         :return:
#         """
#         self.assertEqual(self.user_account.check_user(self.test_user23["email_address"]), True)
#
#     def test_get_user(self):
#         """
#         This method tests the get_user method of the Account class
#         :return:
#         """
#         self.assertEqual(self.user_account.get_user(self.test_user23["email_address"]), 1)
#
#     def test_get_user_name(self):
#         """
#         This method tests the get_user_name method of the Account class
#         :return:
#         """
#         self.assertEqual(self.user_account.get_user_name(
#             self.user_account.accounts[0]["user_id"]), self.test_user23["name"])
#
#     def test_get_check_admin(self):
#         """
#         This method tests the get_check_admin method of the Account class
#         :return:
#         """
#         self.assertEqual(self.user_account.check_admin(self.user_account.accounts[0]["user_id"]), False)
#
#     def test_promote_user(self):
#         """
#         This method tests the promote_user method of the Account class
#         :return:
#         """
#         self.assertEqual(self.user_account.promote_user(self.user_account.accounts[0]["user_id"]),
#                          {"name": "YossiFunke", "email_address": "tinkacalvin@gmail.com",
#                           "password": "Rejo78!ce", "user_id": 1, "admin": True}
#                          )
#
#     def test_check_password(self):
#         """
#         This method tests the check_password method of the Account class
#         :return:
#         """
#         self.assertEqual(self.user_account.check_password(self.test_user23["password"]), True)
#
#     def test_validate_email_address(self):
#         """
#         This method tests the validate_email_address method of the Account class
#         :return:
#         """
#         self.assertEqual(self.user_account.validate_email_address(self.test_user22["email_address"]), True)
#         self.assertEqual(self.user_account.validate_email_address(self.test_user21["email_address"]), False)
#
#
# if __name__ == "__main__":
#     unittest.main()
