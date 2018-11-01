import datetime
from flask import jsonify
from app.api.v1.database import DatabaseConnection


db = DatabaseConnection()


class Sales:
    """This class holds the logic for managing a sale record"""

    def __init__(self, user_id):
        self.user_id = user_id
        self.created_on = datetime.datetime.utcnow()
        self.last_modified = datetime.datetime.utcnow()

    def sale_order(self):
        """This creates a sale record after for a product to be sold"""
        sale_id = db.insert_sale_record(self.user_id, self.created_on, self.last_modified)
        return sale_id


class SaleProduct:
    """This holds logic for managing sales for a particular sale record"""
    def __init__(self, sale_id, user_id, product_id, quantity_to_be_sold, payment_mode, last_modified):
        self.sale_id = sale_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity_to_be_sold = quantity_to_be_sold
        self.payment_mode = payment_mode
        self.last_modified = last_modified

    def check_available_product(self):
        """This checks if there is enough for sale"""
        product = db.select_one('products', 'product_id', self.product_id)
        if 1 <= self.quantity_to_be_sold <= product[3]:
            return True

    def sale_product(self):
        """This creates a sale record after for a product to be sold"""
        db.insert_sales(self.sale_id, self.product_id, self.quantity_to_be_sold, self.payment_mode)
        db.update_product_quantity(self.quantity_to_be_sold, self.last_modified, self.product_id)
        return self.last_modified

    @staticmethod
    def get_sale_record(record_id):
        """
        This fetches a sale record
        """
        global sale_single_record
        sale_record = db.select_one_sale(record_id)
        products_sold = []
        grand_total = 0
        if sale_record:
            for column in sale_record:
                products_sold.append(
                    {
                        'product_id': column[1],
                        'product_name': column[7],
                        'details': column[8],
                        'quantity_sold': column[2],
                        'total_cost': column[3]
                    }
                )
                grand_total += column[3]
                sale_single_record = {
                    'sale_id': int(record_id),
                    'created_on': column[6],
                    'user_id': column[5],
                    'store_attendant': column[9],
                    'products_sold': products_sold,
                    'grand_total': grand_total,
                    'payment_mode': column[4]
                }
            return jsonify(sale_single_record), 200
        else:
            return jsonify({"message": "Sale record of id {} does not exist".format(record_id)}), 404

    @staticmethod
    def get_all_sales():
        """
        This fetches all sale record
        :return:
        """
        all_sales = db.select_all_sales()
        sales_book = []
        for sale in all_sales:
            sale_record = {
                'sale_id': sale[0],
                'user_id': sale[5],
                'created_on': sale[6],
                'product_id': sale[1],
                'product_name': sale[7],
                'store_attendant': sale[9],
                'details': sale[8],
                'quantity_sold': sale[2],
                'total_cost': sale[3],
                'payment_method': sale[4]
            }
            sales_book.append(sale_record)
        return sales_book
