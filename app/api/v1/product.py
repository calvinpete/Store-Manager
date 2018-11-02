from flask import jsonify, request
from app.api.v1 import app
from app.api.v1.account import token_required
from app.api.v1.validator import UserValidator
from app.api.v1.models.products import Product
from app.api.v1.models.accounts import Account
from app.api.v1.database import DatabaseConnection


@app.route('/store-manager/api/v1/products', methods=['POST'])
@token_required
def add_product(current_user):
    if Account.check_admin(current_user) != 'admin':
        return jsonify({"message": "You do not have administrator access"}), 401

    try:

        data = request.get_json()
        if len(data.keys()) != 4:
            return jsonify({"message": "please make sure you have the product_name, quantity, "
                                       "details and price fields only!"}), 400

        product_name = data['product_name']
        quantity = data['quantity']
        details = data['details']
        price = data['price']

        if UserValidator.check_string_input(product_name=product_name):
            return jsonify({"message": "Please note that the product_name value should be a string"}), 400

        if UserValidator.check_string_input(details=details):
            return jsonify({"message": "Please note that the value of details should be a string"}), 400

        if UserValidator.check_integer_input(quantity=quantity):
            return jsonify({"message": "Please note that the value of quantity should be a positive integer"}), 400

        if UserValidator.check_integer_input(price=price):
            return jsonify({"message": "Please note that the value of price should be a positive integer"}), 400

        if UserValidator.check_input_validity(product_name=product_name):
            return jsonify({"message": "Please note that the product_name value is missing"}), 400

        if UserValidator.check_input_validity(details=details):
            return jsonify({"message": "Please note that the value of details is missing"}), 400

        item = Product(product_name, quantity, details, price)

        if not item.check_product_existence():
            return jsonify({"product": item.add_product(), "message": "Product successfully added"}), 201
        else:
            return jsonify({"message": "Product already exists"}), 200
    except KeyError:
        return jsonify({"message": "please make sure you have the product_name, quantity, "
                                   "details and price fields only!"}), 400


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

    try:

        data = request.get_json()
        if len(data.keys()) != 4:
            return jsonify({"message": "please make sure you have the product_name, quantity, "
                                       "details and price fields only!"}), 400
        product_name = data['product_name']
        quantity = data['quantity']
        details = data['details']
        price = data['price']

        if UserValidator.check_string_input(product_name=product_name):
            return jsonify({"message": "Please note that the product_name value should be a string"}), 400

        if UserValidator.check_string_input(details=details):
            return jsonify({"message": "Please note that the value of details should be a string"}), 400

        if UserValidator.check_integer_input(quantity=quantity):
            return jsonify({"message": "Please note that the value of quantity should be a positive integer"}), 400

        if UserValidator.check_integer_input(price=price):
            return jsonify({"message": "Please note that the value of price should be a positive integer"}), 400

        if UserValidator.check_input_validity(product_name=product_name):
            return jsonify({"message": "Please note that the product_name value is missing"}), 400

        if UserValidator.check_input_validity(details=details):
            return jsonify({"message": "Please note that the value of details is missing"}), 400

        item = Product(product_name, quantity, details, price)

        return item.modify_product(product_id)

    except KeyError:
        return jsonify({"message": "please make sure you have the product_name, quantity, "
                                   "details and price fields only!"}), 400


@app.route('/store-manager/api/v1/products/<product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):

    if Account.check_admin(current_user) != 'admin':
        return jsonify({"message": "You do not have administrator access"}), 401

    return Product.delete_product(product_id)


@app.route('/store-manager/api/v1/inventory', methods=['POST'])
@token_required
def stock_product(current_user):

    if Account.check_admin(current_user) != 'admin':
        return jsonify({"message": "You do not have administrator access"}), 401

    try:

        data = request.get_json()
        if len(data.keys()) != 2:
            return jsonify({"message": "please make sure you have the product_id and quantity fields only"}), 400

        product_id = data['product_id']
        quantity = data['quantity']

        if UserValidator.check_integer_input(quantity=quantity):
            return jsonify({"message": "Please note that the value of quantity should be a positive integer"}), 400

        if UserValidator.check_integer_input(product_id=product_id):
            return jsonify({"message": "Please note that the value of product_id should be a positive integer"}), 400

        return Product.stock_product(product_id, quantity)
    except KeyError:
        return jsonify({"message": "please make sure you have the product_id and quantity fields only"}), 400
