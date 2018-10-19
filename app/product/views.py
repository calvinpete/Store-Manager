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
        return jsonify({"message": "Please a enter a string"}), 400

    if staff.check_input_validity(category=category):
        return jsonify({"message": "Value for category is required"}), 400

    if item.check_category(category):
        return jsonify({"message": "The {} Category already exists".format(category)}), 409
    item.create_category(category)
    return jsonify({"message": "{} category successfully created".format(category)}), 201
