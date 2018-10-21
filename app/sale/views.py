from flask import jsonify, request
from app import app
from app.accounts import staff
from app.products import item
from app.sales import staff_sales
from app.account.views import token_required


@app.route('/store-manager/api/v1/sales', methods=['POST'])
@token_required
def create_sale_record(current_user):
    if staff.check_admin(current_user):
        return jsonify({"message": "Only a staff attendant can create a sale record"}), 401

    data = request.get_json()
    if len(data.keys()) != 4:
        return jsonify({"message": "You should have the category, product_id, quantity and sale_type fields"}), 400

    category = data['category']
    product_id = data['product_id']
    quantity = data['quantity']
    sale_type = data['sale_type']

    if staff.check_input_type(
            category=category,
            sale_type=sale_type):
        return jsonify({"message": "Please a enter a string"}), 400

    if item.check_product_input_type(product_id=product_id, quantity=quantity):
        return jsonify({"message": "Please a enter an integer"}), 400

    if staff.check_input_validity(
            category=category,
            sale_type=sale_type):
        return jsonify({"message": "Values are required"}), 400

    try:

        if not staff_sales.check_available_product(category, product_id, quantity):
            return jsonify({"message": "Invalid quantity requested"}), 404

        staff_sales.sale_product(category, product_id, quantity, sale_type, staff.get_user_name(current_user))
        return jsonify({"message": "Sale record successfully created"}), 201

    except KeyError:
        return jsonify({"message": "{} category does not exist".format(category)}), 404

    except IndexError:
        return jsonify({"message": "Product does not exist"}), 404


@app.route('/store-manager/api/v1/sales/<sale_id>', methods=['GET'])
@token_required
def get_single_sale_record(current_user, sale_id):

    try:

        if int(sale_id) <= 0:
            return jsonify({"message": "sale_id should be a positive integer"}), 404

        return jsonify(staff_sales.get_sale_record(staff.get_user_name(current_user), sale_id)), 200

    except IndexError:
        return jsonify({"message": "Sale record does not exist"}), 201


@app.route('/store-manager/api/v1/sales', methods=['GET'])
@token_required
def get_all_sale_records(current_user):

    if not staff.check_admin(current_user):
        return jsonify({"message": "You do not have administrator access"}), 401

    return jsonify(staff_sales.get_all_sales()), 200
