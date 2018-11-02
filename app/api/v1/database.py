import psycopg2
from flask import current_app as app


class DatabaseConnection:
    """This class holds all the methods that create, query, update and delete records in the database"""

    def __init__(self):
        self.connection = psycopg2.connect(
            database="storemanager", user="postgres", password="hs", host="127.0.0.1", port="5432"
        )

        try:
            if app.config['TESTING']:
                self.connection = psycopg2.connect(
                    database="storemanagertestdb", user="postgres", password="hs", host="127.0.0.1", port="5432"
                )

        except Exception as e:
            print(e)

        # for connecting to the database
        self.cursor = self.connection.cursor()
        print("Database successfully connected")

    def create_tables(self):
        """This creates a user table, product table and a sales table"""
        user_table = "CREATE TABLE IF NOT EXISTS users(user_id SERIAL PRIMARY KEY, " \
                     "name VARCHAR(255) NOT NULL, email_address VARCHAR(255) UNIQUE NOT NULL, " \
                     "password VARCHAR(500) NOT NULL, account_type VARCHAR(255) NOT NULL, " \
                     "created_on TIMESTAMP NOT NULL, last_modified TIMESTAMP NOT NULL, " \
                     "delete_status BOOLEAN NOT NULL DEFAULT FALSE);"
        self.cursor.execute(user_table)
        self.connection.commit()

        product_table = "CREATE TABLE IF NOT EXISTS products( product_id SERIAL PRIMARY KEY, " \
                        "product_name VARCHAR(255) NOT NULL, details VARCHAR(255) NOT NULL, " \
                        "quantity NUMERIC NOT NULL, price NUMERIC NOT NULL, created_on TIMESTAMP NOT NULL, " \
                        "last_modified TIMESTAMP NOT NULL, delete_status BOOLEAN NOT NULL DEFAULT FALSE);"
        self.cursor.execute(product_table)
        self.connection.commit()

        sale_point_table = "CREATE TABLE IF NOT EXISTS sale_point (sale_id SERIAL PRIMARY KEY, " \
                           "user_id INT NOT NULL REFERENCES users(user_id), " \
                           "created_on TIMESTAMP NOT NULL, last_modified TIMESTAMP NOT NULL, " \
                           "delete_status BOOLEAN NOT NULL DEFAULT FALSE);"
        self.cursor.execute(sale_point_table)
        self.connection.commit()

        sales_table = "CREATE TABLE IF NOT EXISTS sales (record_id SERIAL PRIMARY KEY, " \
                      "sale_id INT NOT NULL REFERENCES sale_point(sale_id), " \
                      "product_id INT NOT NULL REFERENCES products(product_id), " \
                      "quantity_sold NUMERIC NOT NULL, total_cost NUMERIC NOT NULL, " \
                      "payment_mode VARCHAR(255) NOT NULL, delete_status BOOLEAN NOT NULL DEFAULT FALSE);"
        self.cursor.execute(sales_table)
        self.connection.commit()

    def default_admin_setup(self, *args):
        """This method inserts an admin into the database"""
        name = args[0]
        email_address = args[1]
        password = args[2]
        account_type = args[3]
        created_on = args[4]
        last_modified = args[5]
        select_users = "SELECT * FROM users;"
        self.cursor.execute(select_users)
        an_admin = self.cursor.fetchall()
        if not an_admin:
            insert_user = "INSERT INTO users(name, email_address, password, account_type, created_on, last_modified) " \
                          "VALUES('{}', '{}', '{}', '{}', '{}', '{}');"\
                .format(name, email_address, password, account_type, created_on, last_modified)
            self.cursor.execute(insert_user, (name, email_address, password, account_type, created_on, last_modified))
            self.connection.commit()

    def insert_user(self, *args):
        """This method inserts a new user into the database"""
        name = args[0]
        email_address = args[1]
        password = args[2]
        account_type = args[3]
        created_on = args[4]
        last_modified = args[5]
        insert_user = "INSERT INTO users(name, email_address, password, account_type, created_on, last_modified) " \
                      "VALUES('{}', '{}', '{}', '{}', '{}', '{}');"\
            .format(name, email_address, password, account_type, created_on, last_modified)
        self.cursor.execute(insert_user, (name, email_address, password, account_type, created_on, last_modified))
        self.connection.commit()

    def insert_products(self, *args):
        """This method inserts a product into the database"""
        product_name = args[0]
        details = args[1]
        quantity = args[2]
        price = args[3]
        created_on = args[4]
        last_modified = args[5]
        insert_product = "INSERT INTO products(product_name, details, quantity, price, created_on, last_modified) " \
                         "VALUES('{}', '{}', '{}', '{}', '{}', '{}')RETURNING product_id;"\
            .format(product_name, details, quantity, price, created_on, last_modified)
        self.cursor.execute(insert_product, (product_name, details, quantity, price, created_on, last_modified))
        self.connection.commit()
        column_value = self.cursor.fetchone()[0]
        return column_value

    def insert_sale_record(self, *args):
        """This method captures a sale when a product is sold"""
        user_id = args[0]
        created_on = args[1]
        last_modified = args[2]
        insert_sales = "INSERT INTO sale_point(user_id, created_on, last_modified ) " \
                       "VALUES('{}', '{}', '{}') RETURNING sale_id;".format(user_id, created_on, last_modified)
        self.cursor.execute(insert_sales, (user_id, created_on, last_modified))
        self.connection.commit()
        column_value = self.cursor.fetchone()[0]
        return column_value

    def insert_sales(self, *args):
        """This method inserts a sale record into the database"""
        sale_id = args[0]
        product_id = args[1]
        quantity_sold = args[2]
        total_cost = self.select_one('products', 'product_id', product_id)[4] * quantity_sold
        payment_mode = args[3]
        insert_sales = "INSERT INTO sales(sale_id, product_id, quantity_sold, total_cost, payment_mode) " \
                       "VALUES('{}', '{}', '{}', '{}', '{}');"\
            .format(sale_id, product_id, quantity_sold, total_cost, payment_mode)
        self.cursor.execute(insert_sales, (sale_id, product_id, quantity_sold, payment_mode))
        self.connection.commit()

    def select_all(self, table):
        """This method selects all rows in a table"""
        select_table = "SELECT * FROM {} WHERE delete_status = FALSE;".format(table)
        self.cursor.execute(select_table)
        rows = self.cursor.fetchall()
        return rows

    def select_one(self, table, column, value):
        """This method selects one row in a table given the column matches a specific value"""
        select_row = "SELECT * FROM {} WHERE {}='{}' AND delete_status = FALSE;".format(table, column, value)
        self.cursor.execute(select_row)
        row = self.cursor.fetchone()
        return row

    def select_one_product(self, table, column_1, value_1, column_2, value_2):
        """This method selects one row in a table given the column matches a specific value"""
        select_row = "SELECT * FROM {} WHERE {}='{}' AND {}='{}';".format(table, column_1, value_1, column_2, value_2)
        self.cursor.execute(select_row)
        row = self.cursor.fetchone()
        return row

    def update_product_quantity(self, *args):
        """This method modifies the quantity in the product table after sale"""
        quantity_sold = args[0]
        last_modified = args[1]
        product_id = args[2]
        update_row = "UPDATE products SET quantity = quantity - {}, last_modified = '{}' WHERE product_id ='{}';"\
            .format(quantity_sold, last_modified, product_id)
        self.cursor.execute(update_row)
        self.connection.commit()

    def restock_product_quantity(self, product_id, quantity):
        update_row = "UPDATE products SET quantity = quantity + {} WHERE product_id = '{}';"\
            .format(quantity, product_id)
        self.cursor.execute(update_row, (quantity, product_id))
        self.connection.commit()

    def select_all_sales(self):
        """
        This method selects all rows of the sales table together with:
        - Two columns of the products table
        - One column of the users table
        """
        select_sales = "SELECT sales.sale_id, sales.product_id, sales.quantity_sold, sales.total_cost, " \
                       "sales.payment_mode, sale_point.user_id, sale_point.created_on, products.product_name, " \
                       "products.details, users.name FROM sales " \
                       "INNER JOIN sale_point ON sale_point.sale_id = sales.sale_id " \
                       "INNER JOIN products ON products.product_id = sales.product_id " \
                       "INNER JOIN users ON users.user_id = sale_point.user_id;"
        self.cursor.execute(select_sales)
        rows = self.cursor.fetchall()
        return rows

    def select_one_sale(self, record_id):
        """
        This method selects one row of the sales table together with:
        - Two columns of the products table
        - One column of the users table
        """
        select_sale = "SELECT sales.sale_id, sales.product_id, sales.quantity_sold, sales.total_cost, " \
                      "sales.payment_mode, sale_point.user_id, sale_point.created_on, products.product_name, " \
                      "products.details, users.name FROM sales " \
                      "INNER JOIN sale_point ON sale_point.sale_id = sales.sale_id " \
                      "INNER JOIN products ON products.product_id = sales.product_id " \
                      "INNER JOIN users ON users.user_id = sale_point.user_id " \
                      "WHERE sales.sale_id = {};".format(record_id)
        self.cursor.execute(select_sale, [record_id])
        row = self.cursor.fetchall()
        return row

    def update_product(self, *args):
        """This method selects one row in the products table then modifies all the column values"""
        product_name = args[0]
        details = args[1]
        quantity = args[2]
        price = args[3]
        last_modified = args[4]
        product_id = args[5]
        update_row = "UPDATE products SET product_name = '{}', details = '{}', quantity = '{}', price = '{}', " \
                     "last_modified = '{}' WHERE product_id = '{}';"\
            .format(product_name, details, quantity, price, last_modified, product_id)
        self.cursor.execute(update_row, (product_name, details, quantity, price, last_modified, product_id))
        self.connection.commit()

    def delete_product(self, last_modified, product_id):
        """This method selects one row in the products table then deletes it"""
        delete_row = "UPDATE products SET delete_status = TRUE, last_modified = '{}' WHERE product_id = '{}';"\
            .format(last_modified, product_id)
        self.cursor.execute(delete_row, (last_modified, product_id))
        self.connection.commit()

    def drop_tables(self, table):
        """This method drops a table"""
        drop_table = "DROP TABLE IF EXISTS {} CASCADE;".format(table)
        self.cursor.execute(drop_table)
