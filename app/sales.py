import datetime
from app.products import item


class Sales:
    """This class holds the logic for managing sales"""

    def __init__(self):
        self.sales_records = {}  # A data structure for holding sale records

    def new_record(self, username):
        """
        This creates a list to hold sale records for a single staff attendant
        :param username:
        :return:
        """
        self.sales_records[username] = []
        return self.sales_records

    @staticmethod
    def check_available_product(category, pdt_id, qty):
        """
        This checks if there is enough for sale
        :param category:
        :param qty:
        :param pdt_id:
        :return:
        """
        for product in item.stock[category]:
            if product["product_id"] == pdt_id:
                if product["quantity"] >= qty:
                    return True

    def sale_product(self, category, pdt_id, qty, status, username):
        """
        This creates a sale record after a product is sold
        :param category:
        :param status:
        :param username:
        :param pdt_id:
        :param qty:
        :return:
        """
        for pdt in item.stock[category]:
            if pdt["product_id"] == pdt_id:
                pdt["quantity"] -= qty
                record_id = len(self.sales_records) + 1
                sale_record = {
                    "record_id": record_id,
                    "date of sale": str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")),
                    "product_id": pdt_id,
                    "product_name": pdt["product_name"],
                    "category": category,
                    "quantity_sold": qty,
                    "amount": qty * pdt["price"],
                    "status": status
                }
                self.sales_records[username].append(sale_record)
                return self.sales_records

    def get_sale_record(self, username, record_id):
        """
        This fetches a sale record
        :param username:
        :param record_id:
        :return:
        """
        for record in self.sales_records[username]:
            if record_id == record["record_id"]:
                return record

    def get_all_sales(self):
        """
        This fetches all sale record
        :return:
        """
        return self.sales_records


sales = Sales()
