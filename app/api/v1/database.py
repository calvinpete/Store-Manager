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
                     "email_address VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL), " \
                     "admin BOOLEAN NOT NULL;"
        self.cursor.execute(user_table)
        self.connection.commit()

        product_table = "CREATE TABLE product( product_id SERIAL PRIMARY KEY, product_name VARCHAR(255) NOT NULL, " \
                        "details VARCHAR(255) NOT NULL, quantity NUMERIC NOT NULL, price NUMERIC NOT NULL);"
        self.cursor.execute(product_table)
        self.connection.commit()

        sales_table = "CREATE TABLE sales (record_id SERIAL PRIMARY KEY, date_of_sale TIMESTAMP NOT NULL, " \
                      "product_id INT NOT NULL REFERENCES product(product_id), " \
                      "product_name VARCHAR(255) NOT NULL REFERENCES product(product_name), " \
                      "details VARCHAR(255) NOT NULL REFERENCES product(details), quantity_sold NUMERIC NOT NULL, " \
                      "amount NUMERIC NOT NULL);"
        self.cursor.execute(sales_table)
        self.connection.commit()


if __name__ == "__main__":
    database = DatabaseConnection()
