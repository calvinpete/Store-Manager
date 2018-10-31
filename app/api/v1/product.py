from flask import jsonify, request
from app.api.v1 import app
from app.api.v1.account import token_required
from app.api.v1.validator import UserValidator
from app.api.v1.models.products import Product
from app.api.v1.models.accounts import Account
from app.api.v1.database import DatabaseConnection


db = DatabaseConnection()


# @app.route('/store-manager/api/v1/category', methods=['POST'])
# @token_required
# def create_category(current_user):
#     if not Account.check_admin(current_user):
#         return jsonify({"message": "You do not have administrator access"}), 401
#
#     data = request.get_json()
#
#     if len(data.keys()) != 1:
#         return jsonify({"message": "The category field is missing"}), 400
#
#     category = data['category']
#
#     if staff.check_input_type(category=category):
#         return jsonify({"message": "Please enter a string"}), 400
#
#     if staff.check_input_validity(category=category):
#         return jsonify({"message": "Value for category is required"}), 400
#
#     if item.check_category(category):
#         return jsonify({"message": "The {} Category already exists".format(category)}), 409
#     item.create_category(category)
#     return jsonify({"message": "{} category successfully created".format(category)}), 201


@app.route('/store-manager/api/v1/products', methods=['POST'])
@token_required
def add_product(current_user):
    if Account.check_admin(current_user) != 'admin':
        return jsonify({"message": "You do not have administrator access"}), 401

    data = request.get_json()
    if len(data.keys()) != 4:
        return jsonify({"message": "You should have the product_name, quantity, details and price fields"}), 400

    product_name = data['product_name']
    quantity = data['quantity']
    details = data['details']
    price = data['price']

    if UserValidator.check_string_input(
            product_name=product_name,
            details=details):
        return jsonify({"message": "Please enter a string"}), 400

    if UserValidator.check_integer_input(
            quantity=quantity,
            price=price):
        return jsonify({"message": "Please enter an integer"}), 400

    if UserValidator.check_input_validity(
            product_name=product_name,
            details=details):
        return jsonify({"message": "Values are required"}), 400

    item = Product(product_name, quantity, details, price)

    if not item.check_product_existence():
        item.add_product()
        return jsonify({"message": "Product successfully added"}), 201
    else:
        return jsonify({"message": "{} {}'s quantity has been updated".format(details, product_name)}), 200


@app.route('/store-manager/api/v1/products', methods=['GET'])
@token_required
def get_all_products(current_user):
    return jsonify(Product.get_all_products()), 200


@app.route('/store-manager/api/v1/products/<product_id>', methods=['GET'])
@token_required
def get_single_product(current_user, product_id):

    return Product.get_single_product(product_id)


@app.route('/store-manager/api/v1/products/<product_id>', methods=['PUT'])
@token_required
def modify_product(current_user, product_id):
    if Account.check_admin(current_user) != 'admin':
        return jsonify({"message": "You do not have administrator access"}), 401

    data = request.get_json()
    if len(data.keys()) != 4:
        return jsonify({"message": "You should have the product_name, quantity, details and price fields"}), 400

    product_name = data['product_name']
    quantity = data['quantity']
    details = data['details']
    price = data['price']

    if UserValidator.check_string_input(
            product_name=product_name,
            details=details):
        return jsonify({"message": "Please enter a string"}), 400

    if UserValidator.check_integer_input(
            quantity=quantity,
            price=price):
        return jsonify({"message": "Please enter an integer"}), 400

    if UserValidator.check_input_validity(
            product_name=product_name,
            details=details):
        return jsonify({"message": "Values are required"}), 400

    item = Product(product_name, quantity, details, price)

    if db.select_one('products', 'product_id', product_id) is not None:
        return jsonify({"message": "Product does not exist"}), 404

    item.modify_product(product_id)
    return jsonify({"message": "Product successfully modified"}), 200


@app.route('/store-manager/api/v1/products/<product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):

    if Account.check_admin(current_user) != 'admin':
        return jsonify({"message": "You do not have administrator access"}), 401

    return Product.delete_product(product_id)
