import datetime
from flask import jsonify
from app.api.v1.database import DatabaseConnection


db = DatabaseConnection()


class Product:
    """This class holds the logic for managing inventory"""
    def __init__(self, *args):
        self.product_name = args[0]
        self.quantity = args[1]
        self.details = args[2]
        self.price = args[3]
        self.created_on = datetime.datetime.utcnow()
        self.last_modified = datetime.datetime.utcnow()

    def add_product(self):
        """This adds a product to the inventory"""
        db.insert_products(self.product_name, self.details, self.quantity, self.price, self.created_on,
                           self.last_modified)
        return self.product_name

    def check_product_existence(self):
        """This checks if the product already exists then updates its quantity"""
        product = db.select_one_product('products', 'product_name', self.product_name, 'details', self.details)
        if product is not None:
            db.update_product_quantity('product_name', self.product_name, 'details', self.details, product[3],
                                       self.quantity, self.last_modified)
            return True

    def modify_product(self, product_id):
        """This edits a single product's information"""
        db.update_product(self.product_name, self.details, self.quantity, self.price, self.created_on, product_id)

    @staticmethod
    def get_single_product(product_id):
        """This fetches a single product"""
        product = db.select_one('products', 'product_id', product_id)
        if product:
            return jsonify(
                {
                    'product_id': product[0],
                    'product_name': product[1],
                    'details': product[2],
                    'quantity': product[3],
                    'price': product[4],
                    'created_on': product[5],
                    'last_modified': product[6]
                }
            ), 200
        else:
            return jsonify({"message": "Product does not exist"}), 404

    @staticmethod
    def get_all_products():
        """This fetches all available products"""
        all_products = db.select_all('products')
        inventory = []
        for product in all_products:
            single_item = {
                'product_id': product[0],
                'product_name': product[1],
                'details': product[2],
                'quantity': product[3],
                'price': product[4],
                'created_on': product[5],
                'last_modified': product[6]
            }
            inventory.append(single_item)
        return inventory

    @staticmethod
    def delete_product(product_id):
        """This removes a product from the inventory"""
        product = db.select_one('products', 'product_id', product_id)
        if product:
            db.delete_product(product_id)
            return jsonify({
                "message": "{} of {} successfully removed from the inventory".format(product[1], product[2])
            }), 200
        else:
            return jsonify({"message": "Product does not exist"}), 404
