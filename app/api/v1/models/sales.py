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
        self.quantity_to_be_sold = args[3]
        self.payment_mode = args[4]

    def check_available_product(self):
        """This checks if there is enough for sale"""
        product = db.select_one('products', 'product_id', self.product_id)
        if 1 <= self.quantity_to_be_sold <= product[3]:
            return True

    def sale_product(self):
        """This creates a sale record after a product is sold"""
        db.insert_sales(self.user_id, self.store_attendant, self.date_of_sale, self.product_id,
                        self.quantity_to_be_sold, self.payment_mode)
        sale_record = db.select_one('sales', 'user_id', self.user_id)
        return sale_record[2]

    @staticmethod
    def get_sale_record(record_id):
        """
        This fetches a sale record
        """
        sale_record = db.select_one_sale(record_id)
        products_sold = []
        grand_total = 0
        if sale_record:
            for column in sale_record:
                products_sold.append(
                    {
                        'product_id': column[2],
                        'product_name': column[6],
                        'details': column[7],
                        'quantity_sold': column[3],
                        'total_cost': column[4]
                    }
                )
                grand_total += column[4]
            return jsonify(
                {
                    'record_id': record_id,
                    'date of sale': sale_record[1],
                    'user_id': sale_record[0],
                    'store_attendant': sale_record[8],
                    'products_sold': products_sold,
                    'grand_total': grand_total,
                    'payment_mode': sale_record[5]
                }
            ), 200
        else:
            return jsonify({"message": "Sale record does not exist"}), 404

    @staticmethod
    def get_all_sales():
        """
        This fetches all sale record
        :return:
        """
        all_sales = db.select_all_sales()
        sales_book = {}
        for sale in all_sales:
            sales_book[sale[9]] = {
                'record_id': sale[0],
                'user_id': sale[1],
                'date of sale': sale[2],
                'product_id': sale[3],
                'product_name': sale[7],
                'details': sale[8],
                'quantity_sold': sale[4],
                'total_cost': sale[5],
                'payment_method': sale[6]
            }
        return sales_book
