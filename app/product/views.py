from flask import jsonify, request
from app import app
from app.products import item
from app.accounts import staff
from app.account.views import token_required


@app.route('/store-manager/api/v1/category', methods=['POST'])
@token_required
def create_category(current_user):
    if not staff.check_admin(current_user):
        return jsonify({"message": "You do not have administrator access"}), 401

    data = request.get_json()

    if len(data.keys()) != 1:
        return jsonify({"message": "The category field is missing"}), 400

    category = data['category']

    if staff.check_input_type(category=category):
        return jsonify({"message": "Please enter a string"}), 400

    if staff.check_input_validity(category=category):
        return jsonify({"message": "Value for category is required"}), 400

    if item.check_category(category):
        return jsonify({"message": "The {} Category already exists".format(category)}), 409
    item.create_category(category)
    return jsonify({"message": "{} category successfully created".format(category)}), 201


@app.route('/store-manager/api/v1/<category>/products', methods=['POST'])
@token_required
def add_product(current_user, category):
    if not staff.check_admin(current_user):
        return jsonify({"message": "You do not have administrator access"}), 401

    data = request.get_json()
    if len(data.keys()) != 4:
        return jsonify({"message": "You should have the product_name, quantity, details and price fields"}), 400

    product_name = data['product_name']
    quantity = data['quantity']
    details = data['details']
    price = data['price']

    if staff.check_input_type(
            product_name=product_name,
            details=details):
        return jsonify({"message": "Please enter a string"}), 400

    if item.check_product_input_type(
            quantity=quantity,
            price=price):
        return jsonify({"message": "Please enter an integer"}), 400

    if staff.check_input_validity(
            product_name=product_name,
            details=details):
        return jsonify({"message": "Values are required"}), 400

    try:

        if not item.check_product_existence(category, product_name, details, quantity):
            item.add_product(category, product_name, quantity, details, price)
            return jsonify({"message": "Product successfully added"}), 201
        else:
            return jsonify({"message": "{} {}'s quantity has been updated".format(details, product_name)}), 200

    except KeyError:
        return jsonify({"message": "{} category does not exist".format(category)}), 404


@app.route('/store-manager/api/v1/products', methods=['GET'])
@token_required
def get_all_products(current_user):
    return jsonify(item.get_all_products()), 200


@app.route('/store-manager/api/v1/<category>/products/<product_id>', methods=['GET'])
@token_required
def get_single_product(current_user, category, product_id):

    try:
        if int(product_id) <= 0:
            return jsonify({"message": "Product_id should be a positive integer"}), 404

        return jsonify(item.get_single_product(category, product_id)), 200

    except KeyError:
        return jsonify({"message": "{} category does not exist".format(category)}), 404

    except IndexError:
        return jsonify({"message": "Product does not exist"}), 404
