import psycopg2
from instance.config import app_config


class DatabaseConnection:
    """This class holds all the methods that create, query, update and delete records in the database"""

    def __init__(self):
        self.connection = psycopg2.connect(
            database="storemanager", user="calvin", password="310892", host="127.0.0.1", port="5432"
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        print("Successfully connected to the database")
        try:
            if app_config["testing"]:
                self.connection = psycopg2.connect(
                    database="storemanagertestdb", user="calvin", password="310892", host="127.0.0.1", port="5432"
                )
                self.connection.autocommit = True
                self.cursor = self.connection.cursor()

        except Exception as e:
            print(e)
            print("No connection to the database")

    def create_tables(self):
        """This creates a user table, product table and a sales table"""
        user_table = "CREATE TABLE users (user_id SERIAL PRIMARY KEY, name VARCHAR(255) UNIQUE NOT NULL, " \
                     "email_address VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, " \
                     "admin BOOLEAN NOT NULL DEFAULT FALSE, Date_of_register TIMESTAMP NOT NULL);"
        self.cursor.execute(user_table)
        self.connection.commit()

        product_table = "CREATE TABLE products( product_id SERIAL PRIMARY KEY, product_name VARCHAR(255) NOT NULL, " \
                        "details VARCHAR(255) NOT NULL, quantity NUMERIC NOT NULL, price NUMERIC NOT NULL, " \
                        "Last_Modified TIMESTAMP NOT NULL);"
        self.cursor.execute(product_table)
        self.connection.commit()

        sales_table = "CREATE TABLE sales (record_id SERIAL PRIMARY KEY, date_of_sale TIMESTAMP NOT NULL, " \
                      "product_id INT NOT NULL REFERENCES product(product_id), " \
                      "product_name VARCHAR(255) NOT NULL REFERENCES product(product_name), " \
                      "details VARCHAR(255) NOT NULL REFERENCES product(details), quantity_sold NUMERIC NOT NULL, " \
                      "amount NUMERIC NOT NULL);"
        self.cursor.execute(sales_table)
        self.connection.commit()

    def insert_users(self, *args):
        """This method inserts a new user into the database"""
        name = args[0]
        email_address = args[1]
        password = args[2]
        admin = args[3]
        date_of_register = args[4]
        insert_user = "INSERT INTO users(name, email_address, password, admin, date_of_register) " \
                      "VALUES({}, {}, {}, {});".format(name, email_address, password, admin, date_of_register)
        self.cursor.execute(insert_user, (name, email_address, password, admin, date_of_register))
        self.connection.commit()

    def insert_products(self, *args):
        """This method inserts a product into the database"""
        product_name = args[0]
        details = args[1]
        quantity = args[2]
        price = args[3]
        last_modified = args[4]
        insert_product = "INSERT INTO products(product_name, details, quantity, price, last_modified) " \
                         "VALUES({}, {}, {}, {});".format(product_name, details, quantity, price, last_modified)
        self.cursor.execute(insert_product, (product_name, details, quantity, price, last_modified))
        self.connection.commit()

    def insert_sales(self, *args):
        """This method inserts a sale record into the database"""
        date_of_sale = args[0]
        product_id = args[1]
        product_name = args[2]
        details = args[3]
        quantity_sold = args[4]
        amount = args[5]
        insert_sales = "INSERT INTO sales(date_of_sale, product_id, product_name, details, quantity_sold, amount) " \
                       "VALUES({}, {}, {}, {});".format(date_of_sale, product_id, product_name, details, quantity_sold,
                                                        amount)
        self.cursor.execute(insert_sales, (date_of_sale, product_id, product_name, details, quantity_sold, amount))
        self.connection.commit()


if __name__ == "__main__":
    database = DatabaseConnection()
