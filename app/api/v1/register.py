from flask import jsonify, request
from app.api.v1 import app
from app.api.v1.models.accounts import Account
from app.api.v1.validator import UserValidator
from app.api.v1.account import token_required


@app.route('/store-manager/api/v1/auth/signup', methods=['POST'])
@token_required
def register_staff(current_user):

    if not Account.check_admin(current_user):
        return jsonify({"message": "You do not have administrator access"}), 401

    data = request.get_json()
    if len(data.keys()) != 3:
        return jsonify({"message": "please type in the missing fields"}), 400

    name = data['name']
    email_address = data['email_address']
    password = data['password']
    account_type = data['account_type']

    validate = UserValidator(email_address, password)

    if validate.check_string_input(
            name=name,
            email_address=email_address,
            password=password,
            account_type=account_type):
        return jsonify({"message": "Please enter a string"}), 400

    if validate.check_input_validity(
            name=name,
            email_address=email_address,
            password=password,
            account_type=account_type):
        return jsonify({"message": "Values are required"}), 400

    if not validate.validate_email_address():
        return jsonify({"message": "The email should follow the format of valid emails (johndoe@mail.com)"}), 400

    staff = Account(name, email_address, password, account_type)

    if staff.check_user():
        return jsonify({"message": "User already exists"}), 409
    else:
        user = staff.register()
        return jsonify({"message": "{} has been successfully registered".format(user)}), 201
