# import unittest
# import json
# import datetime
# from app.api.v1.models.accounts import Account
# # from app.api.v1.models.products import Product
# # from app.api.v1.models.sales import SaleProduct, Sales
# from app.api.v1 import app
# from instance.config import app_config
# from app.api.v1.database import DatabaseConnection
#
#
# class TestBase(unittest.TestCase):
#     """
#     This class holds a setup method that creates the environment to run unittests on the app's routes
#     """
#
#     def setUp(self):
#         """
#         This method runs before each task by:
#         - creating an app
#         - a flask test client object
#         - sample data
#         """
#         # flask test client object
#         self.app = app.test_client()
#
#         # app reconfiguration
#         app.config.from_object(app_config["testing"])
#
#         self.test_db = DatabaseConnection()
#
#         # sample data
#         self.test_admin_data = {"email_address": "test_admin@gmail.com", "password": "test_ad"}
#         self.user_account = Account("Mario", "MK@gmail.com", "Li/", "staff_attendant")
#
#         self.test_data09 = {}
#         self.test_data10 = {"name": "Mario", "email_address": "MK@gmail.com", "password": "Li/"}
#         self.test_data11 = {"email_address": "MK@gmail.com", "password": "Li/"}
#         self.test_data101 = {"name": "clint", "email_address": "hope@gmail.com", "password": "///"}
#         self.test_data111 = {"email_address": "hope@gmail.com", "password": "///"}
#         self.test_data12 = {"product_name": "Splash", "quantity": 12, "details": "500ml Mango", "price": 6500}
#         self.test_data13 = {}
#         self.test_data14 = {"product_name": 100, "quantity": 12, "details": "500ml Mango", "price": 6500}
#         self.test_data15 = {"product_name": "Splash", "quantity": 12, "details": 2.3, "price": 6500}
#         self.test_data16 = {"product_name": ["Splash"], "quantity": 12, "details": "500ml Mango", "price": 6500}
#         self.test_data17 = {"product_name": "", "quantity": 12, "details": "500ml Mango", "price": 6500}
#         self.test_data18 = {"product_name": " ", "quantity": 12, "details": "500ml Mango", "price": 6500}
#         self.test_data19 = {"product_name": "Splash", "quantity": 12, "details": "500ml Mango", "price": 6500}
#         self.test_data20 = {"product_name": "Splash", "quantity": "12", "details": "500ml Mango", "price": 6500}
#         self.test_data21 = {"product_name": "Splash", "quantity": 12, "details": "500ml Mango", "price": [6500]}
#         self.test_data22 = {"product_name": "Splash", "quantity": 12.8, "details": "500ml Mango", "price": 6500}
#         self.test_data23 = {"product_name": "Splash", "quantity": 10, "details": "500ml Mango", "price": 6500}
#         self.test_data24 = {"product_name": "Ginger", "quantity": 12, "details": "100ml African spice", "price": 1200}
#         self.test_data25 = {"product_name": "Rice", "quantity": 12, "details": "100ml African spice", "price": 1200}
#         self.test_data26 = {"product_name": "Chicken", "quantity": 12, "details": "100ml African spice", "price": 1200}
#         self.test_data27 = {"product_name": "Coriander", "quantity": 12, "details": "100ml Western", "price": 1200}
#         self.test_data28 = {"product_name": "Riham", "quantity": 12, "details": "300ml Lemon", "price": 1000}
#         self.test_data29 = {"product_name": "Afia", "quantity": 12, "details": "300ml Orange", "price": 3500}
#         self.test_data30 = {"product_name": "Ribena", "quantity": 12, "details": "250ml Black_current", "price": 1200}
#         self.test_data300 = {"product_name": "Ribena", "quantity": 12}
#         self.test_data31 = {"category": "Juices", "product_id": 1, "quantity": 9, "sale_type": "cash"}
#         self.test_data32 = {"category": "Spices", "product_id": 1, "quantity": 3, "sale_type": "credit"}
#         self.test_data320 = {"category": "Lights", "product_id": 1, "quantity": 3, "sale_type": "credit"}
#         self.test_data321 = {"category": "Detergents", "product_id": 1, "quantity": 3, "sale_type": "credit"}
#         self.test_data33 = {}
#         self.test_data34 = {"category": 100, "product_id": 1, "quantity": 9, "sale_type": "cash"}
#         self.test_data35 = {"category": "Drinks", "product_id": 1, "quantity": 9, "sale_type": 67.6}
#         self.test_data36 = {"category": ["Drinks"], "product_id": 1, "quantity": 9, "sale_type": "cash"}
#         self.test_data37 = {"category": "", "product_id": 1, "quantity": 9, "sale_type": "cash"}
#         self.test_data38 = {"category": " ", "product_id": 1, "quantity": 9, "sale_type": "cash"}
#         self.test_data39 = {"category": "Spices", "product_id": 1, "quantity": 12, "sale_type": "cash"}
#         self.test_data40 = {"category": "Drinks", "product_id": "1", "quantity": 9, "sale_type": "cash"}
#         self.test_data41 = {"category": "Drinks", "product_id": 1, "quantity": [9], "sale_type": "cash"}
#         self.test_data42 = {"category": "Drinks", "product_id": 1, "quantity": 9.8, "sale_type": "cash"}
#         self.test_data43 = {"category": "Drinks", "product_id": 1, "quantity": 12, "sale_type": "cash"}
#         self.test_data430 = {"category": "Drinks", "product_id": 1, "quantity": 120, "sale_type": "cash"}
#         self.test_data431 = {"category": "Drinks", "product_id": 1, "quantity": 0, "sale_type": "cash"}
#         self.test_data44 = {"category": "Spices", "product_id": 100, "quantity": 12, "sale_type": "cash"}
#         self.test_data44 = {"category": "Beverages", "product_id": 1, "quantity": 12, "sale_type": "cash"}
#         self.test_user1 = {"name": "Robe", "email_address": "Robe@gmail.com", "password": "R&e"}
#         self.test_user11 = {}
#         self.test_user12 = {"name": 4, "email_address": "JohnP@gmail.com", "password": "Hal0-pEt7&"}
#         self.test_user13 = {"name": 1.9, "email_address": "JohnP@gmail.com", "password": "Hal0-pEt7&"}
#         self.test_user14 = {"name": ["JohnP"], "email_address": "JohnP@gmail.com", "password": "Hal0-pEt7&"}
#         self.test_user15 = {"name": "John Paul", "email_address": 6, "password": "Hal0-pEt7&"}
#         self.test_user16 = {"name": "John Paul", "email_address": 6.8, "password": "Hal0-pEt7&"}
#         self.test_user17 = {"name": "John Paul", "email_address": ["JohnP@gmail.com"], "password": "Hal0-pEt7&"}
#         self.test_user18 = {"name": "John Paul", "email_address": "JohnP@gmail.com", "password": 7}
#         self.test_user19 = {"name": "John Paul", "email_address": "JohnP@gmail.com", "password": 7.9}
#         self.test_user20 = {"name": "John Paul", "email_address": "JohnP@gmail.com", "password": ['hW?5', 8]}
#         self.test_user21 = {"name": "RonaldMark", "email_address": "markronald.com", "password": "marky-6male"}
#         self.test_user22 = {"name": "KingDavid", "email_address": "davidking@gmail.com", "password": "psaLms198?"}
#         self.test_user221 = {"email_address": "davidking@gmail.com", "password": "psaLms198?"}
#         self.test_user23 = {"name": "YossiFunke", "email_address": "tinkacalvin@gmail.com", "password": "Rejo78!ce"}
#         self.test_user231 = {"email_address": "tinkacalvin@gmail.com", "password": "Rce"}
#         self.test_user24 = {"name": "JohnP", "password": "Hal0-pEt7&"}
#         self.test_user25 = {"name": "", "email_address": "JohnP@gmail.com", "password": "Ha90?e=WW"}
#         self.test_user26 = {"name": " ", "email_address": "", "password": "Ha90?e=WW"}
#         self.test_user27 = {"name": "MattHardy", "email_address": "Hardy@gmail.com", "password": "1290"}
#         self.test_user271 = {"email_address": "jamie@gmail.com", "password": "1wpfo"}
#         self.test_user28 = {"username": "dy"}
#         self.test_user29 = {"name": "Joe", "email_address": "Joe@gmail.com", "password": "fqc"}
#         self.test_user30 = {"name": "Land", "email_address": "ecs@gmail.com", "password": "r352"}
#
#         # sample admin user login
#         # login_test_admin = self.app.post('/store-manager/api/v1/auth/login', content_type="application/json",
#         #                                  data=json.dumps(self.test_admin_data))
#         # user_logged_in_data = json.loads(login_test_admin.data.decode())
#         # self.token = user_logged_in_data["token"]
#         #
#         # # sample non admin user
#         # self.app.post('/store-manager/api/v1/register', content_type="application/json",
#         #               data=json.dumps(self.test_data101), headers={'x-access-token': self.token})
#         # login_test_staff = self.app.post('/store-manager/api/v1/auth/login', content_type="application/json",
#         #                                  data=json.dumps(self.test_data111))
#         # staff_logged_in_data = json.loads(login_test_staff.data.decode())
#         # self.token_staff = staff_logged_in_data["token"]
#
#         # # Product class methods
#         # self.goods = Product()
#         # self.goods.create_category(self.test_data01["category"])
#         # self.goods.add_product(
#         #     self.test_data01["category"],
#         #     self.test_data24["product_name"],
#         #     self.test_data24["quantity"],
#         #     self.test_data24["details"],
#         #     self.test_data24["price"])
#         #
#         # # Account class methods
#         # self.user_account.register(self.test_user23["name"], self.test_user23["email_address"],
#         #                            self.test_user23["password"])
#         # self.store_attendant = self.user_account.get_user_name(1)
#         #
#         # # Sales class test methods
#         # self.sample_sales = Sales()
#         # item.create_category(self.test_data08["category"])
#         # item.add_product(
#         #     self.test_data08["category"],
#         #     self.test_data28["product_name"],
#         #     self.test_data28["quantity"],
#         #     self.test_data28["details"],
#         #     self.test_data28["price"]
#         # )
#         # self.sample_sales.sale_product("Drinks", 1, 10, "cash", self.store_attendant)
#
#     def tearDown(self):
#         with app.app_context():
#             db = DatabaseConnection()
#             db.drop_tables('users')
#             db.drop_tables('sales')
#             db.drop_tables('products')
#             db.drop_tables('sale_point')
#
#     def test_existence(self):
#         """
#         This tests existence of an app
#         """
#         self.assertFalse(self.app is None)
#
#     def test_db_creation(self):
#         """This tests an instance of the DatabaseConnection class"""
#         self.assertIsInstance(self.test_db, DatabaseConnection)
#
#
# if __name__ == "__main__":
#     unittest.main()
