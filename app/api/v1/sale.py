from flask import jsonify, request
from app.api.v1 import app
from app.api.v1.models.sales import Sales
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

    data = request.get_json()
    if len(data.keys()) != 4:
        return jsonify({"message": "You should have the category, product_id, quantity and sale_type fields"}), 400

    product_id = data['product_id']
    quantity_to_be_sold = data['quantity_to_be_sold']
    payment_mode = data['payment_mode']

    if UserValidator.check_string_input(payment_mode=payment_mode):
        return jsonify({"message": "Please enter a string"}), 400

    if UserValidator.check_integer_input(product_id=product_id, quantity_to_be_sold=quantity_to_be_sold):
        return jsonify({"message": "Please enter an integer"}), 400

    if UserValidator.check_input_validity(payment_mode=payment_mode):
        return jsonify({"message": "Values are required"}), 400

    staff_sales = Sales(Account.get_user_id(current_user), Account.get_user_name(current_user),
                        product_id, quantity_to_be_sold, payment_mode)

    if db.select_one('products', 'product_id', product_id) is None:
        return jsonify({"message": "Product does not exist"}), 404

    if not staff_sales.check_available_product():
        return jsonify({"message": "Invalid quantity requested"}), 404

    staff_sales.sale_product()
    return jsonify({"message": "Sale record successfully created"}), 201


@app.route('/store-manager/api/v1/sales/<sale_id>', methods=['GET'])
@token_required
def get_single_sale_record(current_user, sale_id):
    return Sales.get_sale_record(sale_id)


@app.route('/store-manager/api/v1/sales', methods=['GET'])
@token_required
def get_all_sale_records(current_user):

    if Account.check_admin(current_user) != 'admin':
        return jsonify({"message": "You do not have administrator access"}), 401

    return jsonify(Sales.get_all_sales()), 200
