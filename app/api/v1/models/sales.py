import datetime
from flask import jsonify
from app.api.v1.database import DatabaseConnection


db = DatabaseConnection()


class Sales:
    """This class holds the logic for managing sale"""

    def __init__(self, *args):
        self.user_id = args[0]
        self.store_attendant = args[1]
        self.date_of_sale = datetime.datetime.utcnow()
        self.product_id = args[2]
        self.quantity_sold = args[3]
        self.payment_mode = args[4]

    def check_available_product(self):
        """This checks if there is enough for sale"""
        product = db.select_one('products', 'product_id', self.product_id)
        if 1 <= self.quantity_sold <= product[3]:
            return True

    def sale_product(self):
        """This creates a sale record after a product is sold"""
        db.insert_sales(self.user_id, self.store_attendant, self.date_of_sale, self.product_id, self.quantity_sold,
                        self.payment_mode)
        sale_record = db.select_one('sales', 'user_id', self.user_id)
        return sale_record[2]

    def get_sale_record(self, record_id):
        """
        This fetches a sale record
        """
        sale_record = db.select_one('sales', 'record_id', record_id)
        product = db.select_one('products', 'product_id', self.product_id)
        if sale_record:
            return jsonify(
                {
                    'record_id': sale_record[0],
                    'date of sale': sale_record[3],
                    'store_attendant': sale_record[2],
                    'product_name': product[1],
                    'details': product[2],
                    'quantity_sold': sale_record[5],
                    'amount': sale_record[6],
                    'payment_method': sale_record[7]
                }
            ), 200
        else:
            return jsonify({"message": "Sale record does not exist"}), 404

    def get_all_sales(self):
        """
        This fetches all sale record
        :return:
        """
        all_sales = db.select_all('sales')
        product = db.select_one('products', 'product_id', self.product_id)
        sales_book = []
        for sale in all_sales:
            single_item = {
                'record_id': sale[0],
                'date of sale': sale[3],
                'store_attendant': sale[2],
                'product_name': product[1],
                'details': product[2],
                'quantity_sold': sale[5],
                'amount': sale[6],
                'payment_method': sale[7]
            }
            sales_book.append(single_item)
        return sales_book
