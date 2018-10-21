from flask import jsonify, request
from app import app
from app.accounts import staff
from app.account.views import token_required


@app.route('/store-manager/api/v1/register', methods=['POST'])
@token_required
def register_staff(current_user):
    if not staff.check_admin(current_user):
        return jsonify({"message": "You do not have administrator access"}), 401

    data = request.get_json()
    if len(data.keys()) != 3:
        return jsonify({"message": "please type in the missing fields"}), 400

    name = data['name']
    email_address = data['email_address']
    password = data['password']

    if staff.check_input_type(
            name=name,
            email_address=email_address,
            password=password):
        return jsonify({"message": "Please a enter a string"}), 400

    if staff.check_input_validity(
            name=name,
            email_address=email_address,
            password=password):
        return jsonify({"message": "Values are required"}), 400

    if not staff.validate_email_address(email_address):
        return jsonify({"message": "The email should follow the format of valid emails (johndoe@mail.com)"}), 400

    if staff.check_user(email_address):
        return jsonify({"message": "Employee already exists"}), 409
    else:
        staff.register(name, email_address, password)
        return jsonify({"message": "Employee successfully registered"}), 201
