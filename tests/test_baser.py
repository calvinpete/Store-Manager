import unittest
import json
from instance.config import app_config
from app.accounts import Account
from app.products import Product
from app.account.views import *
# from app.register.views import *
# from app.sale import views
# from app.product import views


class TestBase(unittest.TestCase):
    """
    This class holds a setup method that creates the environment to run unittests on the app's routes
    """
    def setUp(self):
        """
        This method runs before each task by:
        - creating an app
        - a flask test client object
        - sample data
        """
        # app reconfiguration
        app.config.from_object(app_config["testing"])

        # flask test client object
        self.app = app.test_client()

        # sample data
        self.test_data01 = {"category": "Spices"}
        self.test_data02 = {"category": 5}
        self.test_data03 = {"category": 6.8}
        self.test_data04 = {"category": ['Snacks', 8]}
        self.test_data05 = {"category": ""}
        self.test_data07 = {"category": " "}
        self.test_data08 = {"category": "Drinks"}
        self.test_data09 = {}
        self.test_data10 = {"name": "Mario", "email_address": "MK@gmail.com", "password": "Li/"}
        self.test_data11 = {"email_address": "MK@gmail.com", "password": "Li/"}
        self.test_data12 = {"product_name": "Splash", "quantity": 12, "details": "500ml Mango", "price": 6500}
        self.test_data13 = {}
        self.test_data14 = {"product_name": 100, "quantity": 12, "details": "500ml Mango", "price": 6500}
        self.test_data15 = {"product_name": "Splash", "quantity": 12, "details": 2.3, "price": 6500}
        self.test_data16 = {"product_name": ["Splash"], "quantity": 12, "details": "500ml Mango", "price": 6500}
        self.test_data17 = {"product_name": "", "quantity": 12, "details": "500ml Mango", "price": 6500}
        self.test_data18 = {"product_name": " ", "quantity": 12, "details": "500ml Mango", "price": 6500}
        self.test_data19 = {"product_name": "Splash", "quantity": 12, "details": "500ml Mango", "price": 6500}
        self.test_data20 = {"product_name": "Splash", "quantity": "12", "details": "500ml Mango", "price": 6500}
        self.test_data21 = {"product_name": "Splash", "quantity": 12, "details": "500ml Mango", "price": [6500]}
        self.test_data22 = {"product_name": "Splash", "quantity": 12.8, "details": "500ml Mango", "price": 6500}
        self.test_data23 = {"product_name": "Splash", "quantity": 10, "details": "500ml Mango", "price": 6500}
        self.test_data24 = {"product_name": "Ginger", "quantity": 12, "details": "100ml African spice", "price": 1200}
        self.test_data25 = {"product_name": "Rice", "quantity": 12, "details": "100ml African spice", "price": 1200}
        self.test_data26 = {"product_name": "Chicken", "quantity": 12, "details": "100ml African spice", "price": 1200}
        self.test_data27 = {"product_name": "Coriander", "quantity": 12, "details": "100ml Western", "price": 1200}
        self.test_data28 = {"product_name": "Riham", "quantity": 12, "details": "300ml Lemon", "price": 1000}
        self.test_data29 = {"product_name": "Afia", "quantity": 12, "details": "300ml Orange", "price": 3500}
        self.test_data30 = {"product_name": "Ribena", "quantity": 12, "details": "250ml Black_current", "price": 1200}
        self.test_data31 = {"category": "Drinks", "product_id": 1, "quantity": 9, "sale_type": "cash"}
        self.test_data32 = {"category": "Spices", "product_id": 1, "quantity": 3, "sale_type": "credit"}
        self.test_data33 = {}
        self.test_data34 = {"category": 100, "product_id": 1, "quantity": 9, "sale_type": "cash"}
        self.test_data35 = {"category": "Drinks", "product_id": 1, "quantity": 9, "sale_type": 67.6}
        self.test_data36 = {"category": ["Drinks"], "product_id": 1, "quantity": 9, "sale_type": "cash"}
        self.test_data37 = {"category": "", "product_id": 1, "quantity": 9, "sale_type": "cash"}
        self.test_data38 = {"category": " ", "product_id": 1, "quantity": 9, "sale_type": "cash"}
        self.test_data39 = {"category": "Spices", "product_id": 1, "quantity": 12, "sale_type": "cash"}
        self.test_data40 = {"category": "Drinks", "product_id": "1", "quantity": 9, "sale_type": "cash"}
        self.test_data41 = {"category": "Drinks", "product_id": 1, "quantity": [9], "sale_type": "cash"}
        self.test_data42 = {"category": "Drinks", "product_id": 1, "quantity": 9.8, "sale_type": "cash"}
        self.test_data43 = {"category": "Drinks", "product_id": 1, "quantity": 12, "sale_type": "cash"}
        self.test_data44 = {"category": "Spices", "product_id": 100, "quantity": 12, "sale_type": "cash"}
        self.test_data44 = {"category": "Beverages", "product_id": 1, "quantity": 12, "sale_type": "cash"}
        self.user_account = Account()
        self.test_user1 = {"name": "Robe", "email_address": "Robe@gmail.com", "password": "R&e"}
        self.test_user11 = {}
        self.test_user12 = {"name": 4, "email_address": "JohnP@gmail.com", "password": "Hal0-pEt7&"}
        self.test_user13 = {"name": 1.9, "email_address": "JohnP@gmail.com", "password": "Hal0-pEt7&"}
        self.test_user14 = {"name": ["JohnP"], "email_address": "JohnP@gmail.com", "password": "Hal0-pEt7&"}
        self.test_user15 = {"name": "John Paul", "email_address": 6, "password": "Hal0-pEt7&"}
        self.test_user16 = {"name": "John Paul", "email_address": 6.8, "password": "Hal0-pEt7&"}
        self.test_user17 = {"name": "John Paul", "email_address": ["JohnP@gmail.com"], "password": "Hal0-pEt7&"}
        self.test_user18 = {"name": "John Paul", "email_address": "JohnP@gmail.com", "password": 7}
        self.test_user19 = {"name": "John Paul", "email_address": "JohnP@gmail.com", "password": 7.9}
        self.test_user20 = {"name": "John Paul", "email_address": "JohnP@gmail.com", "password": ['hW?5', 8]}
        self.test_user21 = {"name": "RonaldMark", "email_address": "markronald.com", "password": "marky-6male"}
        self.test_user22 = {"name": "KingDavid", "email_address": "davidking@gmail.com", "password": "psaLms198?"}
        self.test_user23 = {"name": "YossiFunke", "email_address": "tinkacalvin@gmail.com", "password": "Rejo78!ce"}
        self.test_user24 = {"name": "JohnP", "password": "Hal0-pEt7&"}
        self.test_user25 = {"name": "", "email_address": "JohnP@gmail.com", "password": "Ha90?e=WW"}
        self.test_user26 = {"name": " ", "email_address": "", "password": "Ha90?e=WW"}

        # sample user
        self.app.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                      data=json.dumps(self.test_data10))
        login_test_user = self.app.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                        data=json.dumps(self.test_data11))
        user_logged_in_data = json.loads(login_test_user.data.decode())
        self.token = user_logged_in_data["token"]

        # Product class test methods
        self.goods = Product()
        self.goods.create_category(self.test_data01["category"])
        self.goods.add_product(
            self.test_data01["category"],
            self.test_data24["product_name"],
            self.test_data24["quantity"],
            self.test_data24["details"],
            self.test_data24["price"])

    def test_existence(self):
        """
        This tests existence of an app
        """
        self.assertFalse(self.app is None)


if __name__ == "__main__":
    unittest.main()
