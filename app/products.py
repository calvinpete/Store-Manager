class Product:
    """This class holds the logic for managing inventory"""
    def __init__(self):
        self.stock = []  # A list to hold available products

    def add_product(self, product_name, category, quantity, unit_quantity, cost, price):
        """
        This adds a product to the inventory
        :param unit_quantity:
        :param product_name:
        :param category:
        :param quantity:
        :param cost:
        :param price:
        :return:
        """
        product_id = len(self.stock) + 1
        product = {
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "quantity": quantity,
            "unit_quantity": unit_quantity,
            "cost": cost,
            "price": price
        }
        self.stock.append(product)
        return self.stock

    def check_product(self, product_id):
        """
        This checks if the product exists
        :param product_id:
        :return:
        """
        for product in self.stock:
            if product_id == product["product_id"]:
                return True

    def get_product(self, product_id):
        """
        This fetches a product's details
        :param product_id:
        :return:
        """
        for product in self.stock:
            if self.check_product(product_id):
                return product

    def get_all_products(self):
        """
        This fetches all available products
        :return:
        """
        return self.stock
