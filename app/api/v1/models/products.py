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
        product_id = db.insert_products(self.product_name, self.details, self.quantity, self.price,
                                        self.created_on, self.last_modified)
        product = db.select_one('products', 'product_id', product_id)
        return {
            'product_id': product[0],
            'created_on': product[5],
            'last_modified': product[6],
            'product_name': product[1],
            'details': product[2],
            'quantity': product[3],
            'price': product[4]
        }

    def check_product_existence(self):
        """This checks if the product already exists then updates its quantity"""
        product = db.select_one_product('products', 'product_name', self.product_name, 'details', self.details)
        if product is not None:
            return True

    def modify_product(self, product_id):
        """This edits a single product's information"""
        product = db.select_one('products', 'product_id', product_id)
        if product:
            db.update_product(self.product_name, self.details, self.quantity, self.price, self.last_modified,
                              product_id)
            new_product = db.select_one('products', 'product_id', product_id)
            return jsonify({
                "message": "Product successfully modified",
                "old_product_info": {
                    'product_id': product[0],
                    'created_on': product[5],
                    'last_modified': product[6],
                    'product_name': product[1],
                    'details': product[2],
                    'quantity': product[3],
                    'price': product[4]
                },
                "new_product_info": {
                    'product_id': new_product[0],
                    'created_on': new_product[5],
                    'last_modified': new_product[6],
                    'product_name': new_product[1],
                    'details': new_product[2],
                    'quantity': new_product[3],
                    'price': new_product[4]
                }
            }), 200
        else:
            return jsonify({"message": "Product with id {} does not exist".format(product_id)}), 404

    @staticmethod
    def stock_product(product_id, quantity):
        """This restocks a product"""
        product = db.select_one('products', 'product_id', product_id)
        if product:
            db.restock_product_quantity(product_id, quantity)
            return jsonify({"message": "Product successfully restocked"}), 200
        else:
            return jsonify({"message": "Product of id {} does not exist".format(product_id)}), 404

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
            return jsonify({"message": "Product of id {} does not exist".format(product_id)}), 404

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
            db.delete_product(datetime.datetime.utcnow(), product_id)
            return jsonify({
                "message": "{} of {} successfully removed from the inventory".format(product[1], product[2])
            }), 200
        else:
            return jsonify({"message": "Product of id {} does not exist".format(product_id)}), 404
