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

    def add_product(self, category, product_name, quantity, cost, price):
        """
        This adds a product to the inventory
        :param category:
        :param product_name:
        :param quantity:
        :param cost:
        :param price:
        :return:
        """
        product_id = len(self.stock[category]) + 1
        product = {
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "cost": cost,
            "price": price
        }
        self.stock[category].append(product)
        return self.stock

    def check_product(self, category, product_id):
        """
        This checks if the product exists
        :param category:
        :param product_id:
        :return:
        """
        for product in self.stock[category]:
            if product_id == product["product_id"]:
                return True

    def get_product(self, category, product_id):
        """
        This fetches a product's details
        :param category:
        :param product_id:
        :return:
        """
        for product in self.stock[category]:
            if self.check_product(category, product_id):
                return product

    def get_all_products(self):
        """
        This fetches all available products
        :return:
        """
        return self.stock


item = Product()
