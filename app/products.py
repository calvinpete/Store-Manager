class Product:
    """This class holds the logic for managing inventory"""
    def __init__(self):
        self.stock = {}  # A data structure to hold available products

    def create_category(self, category):
        """
        This creates a list to hold products for that category
        :param category:
        :return:
        """
        self.stock[category] = []

    def check_category(self, category):
        """
        This checks if the category exists
        :param category:
        :return:
        """
        for key in self.stock.keys():
            if category == key:
                return True

    def add_product(self, category, product_name, quantity, details, price):
        """
        This adds a product to the inventory
        :param category:
        :param product_name:
        :param quantity:
        :param details:
        :param price:
        :return:
        """
        product_id = len(self.stock[category]) + 1
        product = {
            "product_id": product_id,
            "product_name": product_name,
            "details": details,
            "quantity": quantity,
            "price": price
        }
        self.stock[category].append(product)
        return self.stock

    @staticmethod
    def check_product_input_type(**kwargs):
        """
        This checks if the product_id, quantity and price are not integers
        :param kwargs:
        :return:
        """
        for (k, v) in kwargs.items():
            if isinstance(v, str) or isinstance(v, float) or isinstance(v, list):
                return True

    def check_product_existence(self, category, product_name, details):
        """
        This checks if the product already exists
        :param product_name:
        :param details:
        :param category:
        :return:
        """
        for product in self.stock[category]:
            if product_name == product["product_name"] and product["details"] == details:
                return True

    def get_single_product(self, category, product_id):
        """
        This fetches a single product
        :param category:
        :param product_id:
        :return:
        """
        return self.stock[category][int(product_id) - 1]

    def get_all_products(self):
        """
        This fetches all available products
        :return:
        """
        return self.stock


item = Product()
