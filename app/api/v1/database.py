import psycopg2
from flask import current_app as app


class DatabaseConnection:
    """This class holds all the methods that create, query, update and delete records in the database"""

    def __init__(self):
        self.connection = psycopg2.connect(
            database="storemanager", user="calvin", password="310892", host="127.0.0.1", port="5432"
        )

        try:
            if app.config['TESTING']:
                self.connection = psycopg2.connect(
                    database="storemanagertestdb", user="calvin", password="310892", host="127.0.0.1", port="5432"
                )

        except Exception as e:
            print(e)

        # for connecting to the database
        self.cursor = self.connection.cursor()
        print("Database successfully connected")

    def create_tables(self):
        """This creates a user table, product table and a sales table"""
        user_table = "CREATE TABLE IF NOT EXISTS users(user_id SERIAL PRIMARY KEY, " \
                     "name VARCHAR(255) UNIQUE NOT NULL, email_address VARCHAR(255) UNIQUE NOT NULL, " \
                     "password VARCHAR(255) NOT NULL, account_type VARCHAR(255) NOT NULL, " \
                     "Date_of_register TIMESTAMP NOT NULL);"
        self.cursor.execute(user_table)
        self.connection.commit()

        product_table = "CREATE TABLE IF NOT EXISTS products( product_id SERIAL PRIMARY KEY, " \
                        "product_name VARCHAR(255) NOT NULL, details VARCHAR(255) NOT NULL, " \
                        "quantity NUMERIC NOT NULL, price NUMERIC NOT NULL, Last_Modified TIMESTAMP NOT NULL);"
        self.cursor.execute(product_table)
        self.connection.commit()

        sales_table = "CREATE TABLE IF NOT EXISTS sales (record_id SERIAL PRIMARY KEY, " \
                      "user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE, " \
                      "store_attendant VARCHAR(255) UNIQUE NOT NULL, date_of_sale TIMESTAMP NOT NULL, " \
                      "product_id INT NOT NULL REFERENCES products(product_id) ON DELETE CASCADE, " \
                      "quantity_sold NUMERIC NOT NULL, total_cost NUMERIC NOT NULL, " \
                      "payment_mode VARCHAR(255) NOT NULL);"
        self.cursor.execute(sales_table)
        self.connection.commit()

    def default_admin_setup(self, *args):
        """This method inserts an admin into the database"""
        name = args[0]
        email_address = args[1]
        password = args[2]
        account_type = args[3]
        date_of_register = args[4]
        select_users = "SELECT * FROM users;"
        self.cursor.execute(select_users)
        an_admin = self.cursor.fetchall()
        if not an_admin:
            insert_user = "INSERT INTO users(name, email_address, password, account_type, date_of_register) " \
                          "VALUES('{}', '{}', '{}', '{}', '{}');".format(name, email_address, password, account_type,
                                                                         date_of_register)
            self.cursor.execute(insert_user, (name, email_address, password, account_type, date_of_register))
            self.connection.commit()

    def insert_user(self, *args):
        """This method inserts a new user into the database"""
        name = args[0]
        email_address = args[1]
        password = args[2]
        account_type = args[3]
        date_of_register = args[4]
        insert_user = "INSERT INTO users(name, email_address, password, account_type, date_of_register) " \
                      "VALUES('{}', '{}', '{}', '{}', '{}');".format(name, email_address, password, account_type,
                                                                     date_of_register)
        self.cursor.execute(insert_user, (name, email_address, password, account_type, date_of_register))
        self.connection.commit()

    def insert_products(self, *args):
        """This method inserts a product into the database"""
        product_name = args[0]
        details = args[1]
        quantity = args[2]
        price = args[3]
        last_modified = args[4]
        insert_product = "INSERT INTO products(product_name, details, quantity, price, last_modified) " \
                         "VALUES('{}', '{}', '{}', '{}', '{}');".format(product_name, details, quantity, price,
                                                                        last_modified)
        self.cursor.execute(insert_product, (product_name, details, quantity, price, last_modified))
        self.connection.commit()

    def insert_sales(self, *args):
        """This method inserts a sale record into the database"""
        user_id = args[0]
        store_attendant = args[1]
        date_of_sale = args[2]
        product_id = args[3]
        quantity_sold = args[4]
        total_cost = self.select_one('products.price', 'product_id', product_id)[4]
        payment_mode = args[5]
        insert_sales = "INSERT INTO sales(user_id, store_attendant, date_of_sale, product_id, quantity_sold, " \
                       "total_cost, payment_mode) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}');"\
            .format(user_id, store_attendant, date_of_sale, product_id, quantity_sold, total_cost, payment_mode)
        self.cursor.execute(insert_sales, (user_id, store_attendant, date_of_sale, product_id, quantity_sold,
                                           payment_mode))
        self.connection.commit()

    def select_all(self, table):
        """This method selects all rows in a table"""
        select_table = "SELECT * FROM {};".format(table)
        self.cursor.execute(select_table)
        rows = self.cursor.fetchall()
        return rows

    def select_one(self, table, column, value):
        """This method selects one row in a table given the column matches a specific value"""
        select_row = "SELECT * FROM {} WHERE {}='{}';".format(table, column, value)
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
        """This method selects one row in a table given the column then modifies the column value"""
        column_1 = args[0]
        value_1 = args[1]
        column_2 = args[2]
        value_2 = args[3]
        old_quantity = args[4]
        new_quantity = args[5]
        value_3 = args[6]
        update_row = "UPDATE products SET quantity = {} + {}, Last_Modified = '{}' WHERE {}='{}' AND {}='{}';"\
            .format(old_quantity, new_quantity, value_3, column_1, value_1, column_2, value_2)
        self.cursor.execute(update_row)
        self.connection.commit()

    def select_all_sales(self):
        """
        This method selects all rows of the sales table together with:
        - Two columns of the products table
        - One column of the users table
        """
        select_sales = "SELECT sales.record_id, sales.user_id, sales.date_of_sale, sales.product_id, " \
                       "sales.quantity_sold, sales.total_cost, sales.payment_mode, products.product_name, " \
                       "products.details, users.name FROM sales " \
                       "INNER JOIN products ON products.product_id = sales.product_id " \
                       "INNER JOIN users ON users.user_id = sales.user_id ORDER BY sales.date_of_sale;"
        self.cursor.execute(select_sales)
        rows = self.cursor.fetchall()
        return rows

    def select_one_sale(self, record_id):
        """
        This method selects one row of the sales table together with:
        - Two columns of the products table
        - One column of the users table
        """
        select_sale = "SELECT sales.user_id, sales.date_of_sale, sales.product_id, sales.quantity_sold, " \
                      "sales.total_cost, sales.payment_mode, products.product_name, products.details, " \
                      "users.name FROM sales INNER JOIN products ON products.product_id = sales.product_id " \
                      "INNER JOIN users ON users.user_id = sales.user_id " \
                      "WHERE sales.record_id = '{}';".format(record_id)
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
        update_row = "UPDATE product_name = '{}', details = '{}', quantity = '{}', price = '{}', " \
                     "last_modified = '{}' WHERE product_id = '{}';"\
            .format(product_name, details, quantity, price, last_modified, product_id)
        self.cursor.execute(update_row, (product_name, details, quantity, price, last_modified, product_id))
        self.connection.commit()

    def delete_product(self, product_id):
        """This method selects one row in the products table then deletes it"""
        delete_row = "DELETE FROM products WHERE 'product_id' = {}".format(product_id)
        self.cursor.execute(delete_row, [product_id])
        self.connection.commit()

    def before_delete_product(self):
        """This method keeps a copy of the sale_record just before a product is deleted"""
        sale_copies = "CREATE TABLE IF NOT EXISTS sales_copies (record_id SERIAL PRIMARY KEY, " \
                      "user_id, store_attendant VARCHAR(255) UNIQUE NOT NULL, date_of_sale TIMESTAMP NOT NULL, " \
                      "product_id INT NOT NULL, quantity_sold NUMERIC NOT NULL, total_cost NUMERIC NOT NULL, " \
                      "payment_mode VARCHAR(255) NOT NULL);"
        self.cursor.execute(sale_copies)
        self.connection.commit()

        trigger_function = "CREATE FUNCTION copy_sale() RETURNS trigger AS $BODY$" \
                           "BEGIN " \
                           "INSERT INTO sales_copies VALUES(OLD.record_id, OLD.user_id, OLD.store_attendant, " \
                           "OLD.date_of_sale, OLD.product_id, OLD.quantity_sold, OLD.total_cost, OLD.payment_mode)" \
                           "RETURN OLD;" \
                           "END;" \
                           "$BODY$;"
        self.cursor.execute(trigger_function)
        self.connection.commit()

        delete_trigger = "CREATE TRIGGER copy_deleted_sale BEFORE DELETE ON products FOR EACH ROW " \
                         "EXECUTE PROCEDURE copy_sale();"
        self.cursor.execute(delete_trigger)
        self.connection.commit()

    def drop_tables(self, table):
        """This method drops a table"""
        drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table)
        self.cursor.execute(drop_table)
