import datetime
from app.products import item


class Sales:
    """This class holds the logic for managing sale"""

    def __init__(self):
        self.sales_records = {}  # A data structure for holding sale records

    @staticmethod
    def check_available_product(category, pdt_id, qty):
        """
        This checks if there is enough for sale
        :param category:
        :param qty:
        :param pdt_id:
        :return:
        """
        pdt = item.stock[category][int(pdt_id) - 1]
        if int(pdt["quantity"]) >= int(qty) >= 1:
            return True

    def sale_product(self, category, pdt_id, qty, sale_type, name):
        """
        This creates a sale record after a product is sold
        :param category:
        :param sale_type:
        :param name:
        :param pdt_id:
        :param qty:
        :return:
        """
        pdt = item.stock[category][int(pdt_id)-1]
        pdt["quantity"] = int(pdt["quantity"]) - int(qty)
        record_id = len(self.sales_records) + 1
        sale_record = {
            "record_id": record_id,
            "date of sale": str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")),
            "product_id": pdt_id,
            "product_name": pdt["product_name"],
            "category": category,
            "details": pdt["details"],
            "quantity_sold": qty,
            "amount": int(qty) * int(pdt["price"]),
            "sale_type": sale_type
        }

        for key in self.sales_records.keys():
            if name == key:
                self.sales_records[name].append(sale_record)
                return self.sales_records
        else:
            self.sales_records[name] = []  # A list to hold sale records for a single staff attendant
            self.sales_records[name].append(sale_record)
            return self.sales_records

    def get_sale_record(self, name, record_id):
        """
        This fetches a sale record
        :param name:
        :param record_id:
        :return:
        """
        return self.sales_records[name][int(record_id) - 1]

    def get_all_sales(self):
        """
        This fetches all sale record
        :return:
        """
        return self.sales_records


staff_sales = Sales()
