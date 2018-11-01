from flask import jsonify, request
from app.api.v1 import app
from app.api.v1.models.sales import Sales, SaleProduct
from app.api.v1.database import DatabaseConnection
from app.api.v1.validator import UserValidator
from app.api.v1.models.accounts import Account
from app.api.v1.account import token_required


db = DatabaseConnection()


@app.route('/store-manager/api/v1/sales', methods=['POST'])
@token_required
def create_sale_record(current_user):
    if Account.check_admin(current_user) != 'store_attendant':
        return jsonify({"message": "Only a staff attendant can create a sale record"}), 401

    try:

        data = request.get_json()
        if len(data.keys()) != 2:
            return jsonify({"message": "Please make sure you have the shopping cart and payment_mode fields only"}), 400

        shopping_cart = data['products']
        payment_mode = data['payment_mode']

        if len(shopping_cart) == 0:
            return jsonify({"message": "Please add a product in this format "
                                       "{'product_id': 2 and 'quantity_to_be_sold': 2}"}), 400

        if UserValidator.check_string_input(payment_mode=payment_mode):
            return jsonify({"message": "Please note that the value of payment mode should be a string"}), 400

        if UserValidator.check_input_validity(payment_mode=payment_mode):
            return jsonify({"message": "Please make sure you have the value of payment mode"}), 400

        sale_order_id = Sales(Account.get_user_id(current_user))
        code = sale_order_id.sale_order()

        for product in shopping_cart:
            product_id = product.get('product_id')
            quantity_to_be_sold = product.get('quantity_to_be_sold')

            try:
                if len(product) != 2:
                    return jsonify(
                        {"message": "Please make sure you have the product_id and "
                                    "quantity_to_be_sold fields only"}), 400

                if UserValidator.check_integer_input(product_id=product_id):
                    return jsonify({"message": "Please note that the value of product_id "
                                               "should be a positive integer"}), 400

                if UserValidator.check_integer_input(quantity_to_be_sold=quantity_to_be_sold):
                    return jsonify({"message": "Please note that the value of quantity_to_be_sold "
                                               "should be a positive integer"}), 400

                staff_sales = SaleProduct(code, Account.get_user_id(current_user), product_id,
                                          quantity_to_be_sold, payment_mode, sale_order_id.last_modified)

                if db.select_one('products', 'product_id', product_id) is None:
                    return jsonify({"message": "Product does not exist"}), 404

                if not staff_sales.check_available_product():
                    return jsonify({"message": "Invalid quantity requested"}), 404

                staff_sales.sale_product()
            except KeyError:
                return jsonify({"message": "Please make sure you have the product_id and "
                                           "quantity_to_be_sold fields only"}), 400

        return jsonify({"message": "Sale record successfully created"}), 201

    except KeyError:
        return jsonify({"message": "Please make sure you have the shopping cart and payment_mode fields only"}), 400


@app.route('/store-manager/api/v1/sales/<sale_id>', methods=['GET'])
@token_required
def get_single_sale_record(current_user, sale_id):
    return SaleProduct.get_sale_record(sale_id)


@app.route('/store-manager/api/v1/sales', methods=['GET'])
@token_required
def get_all_sale_records(current_user):

    if Account.check_admin(current_user) != 'admin':
        return jsonify({"message": "You do not have administrator access"}), 401

    return jsonify(SaleProduct.get_all_sales()), 200
