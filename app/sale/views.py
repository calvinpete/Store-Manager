from flask import jsonify, request
from app import app
from app.accounts import staff
from app.sales import staff_sales
from app.account.views import token_required


@app.route('/store-manager/api/v1/sales', methods=['POST'])
@token_required
def create_sale_record(current_user):
    if staff.check_admin(current_user):
        return jsonify({"message": "Only a staff attendant can create a sale record"}), 401

    data = request.get_json()
    if len(data.keys()) != 4:
        return jsonify({"message": "You should have the category, product_id, quantity and status fields"}), 400

    category = data['category']
    product_id = data['product_id']
    quantity = data['quantity']
    sale_type = data['sale_type']

    if staff.check_input_type(
            category=category,
            product_id=product_id,
            quantity=quantity,
            slae_type=sale_type):
        return jsonify({"message": "Please a enter a string"}), 400

    if staff.check_input_validity(
            category=category,
            product_id=product_id,
            quantity=quantity,
            sale_type=sale_type):
        return jsonify({"message": "Values are required"}), 400

    try:

        if not staff_sales.check_available_product(category, product_id, quantity):
            return jsonify({"message": "There is not enough to sale"}), 404

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
        return jsonify(staff_sales.get_sale_record(staff.get_user_name(current_user), sale_id)), 200

    except IndexError:
        return jsonify({"message": "Sale record does not exist"}), 201
