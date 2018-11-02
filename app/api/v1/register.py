from flask import jsonify, request
from app.api.v1 import app
from app.api.v1.models.accounts import Account
from app.api.v1.validator import UserValidator
from app.api.v1.account import token_required
from werkzeug.security import generate_password_hash


@app.route('/store-manager/api/v1/auth/signup', methods=['POST'])
@token_required
def register_staff(current_user):

    if not Account.check_admin(current_user):
        return jsonify({"message": "You do not have administrator access"}), 401

    try:

        data = request.get_json()
        if len(data.keys()) != 4:
            return jsonify({"message": "please make sure you have the name, email_address, password and "
                                       "account_type fields only!"}), 400

        name = data['name']
        email_address = data['email_address']
        password = data['password']
        account_type = data['account_type']

        validate = UserValidator(email_address, password)

        if UserValidator.check_string_input(name=name):
            return jsonify({"message": "Please note that the value of name should be a string"}), 400

        if UserValidator.check_string_input(email_address=email_address):
            return jsonify({"message": "Please note that the value of email_address should be a string"}), 400

        if UserValidator.check_string_input(password=password):
            return jsonify({"message": "Please note that the value of password should be a string"}), 400

        if UserValidator.check_string_input(account_type=account_type):
            return jsonify({"message": "Please note that the account_type value should be a string"}), 400

        if UserValidator.check_input_validity(name=name):
            return jsonify({"message": "Please note that the value of name is missing"}), 400

        if UserValidator.check_input_validity(email_address=email_address):
            return jsonify({"message": "Please note that the value of email_address is missing"}), 400

        if UserValidator.check_input_validity(password=password):
            return jsonify({"message": "Please note that the value of password is missing"}), 400

        if UserValidator.check_input_validity(account_type=account_type):
            return jsonify({"message": "Please note that the account_type value is missing"}), 400

        if not validate.validate_email_address():
            return jsonify({"message": "The email should follow the format of valid emails (johndoe@mail.com)"}), 400

        staff = Account(name, email_address, generate_password_hash(password), account_type)

        if staff.check_user():
            return jsonify({"message": "{} is already registered".format(name)}), 409
        else:
            user = staff.register()
            return jsonify({"message": "{} has been successfully registered".format(user)}), 201

    except KeyError:
        return jsonify({"message": "please make sure you have the name, email_address, password and "
                                   "account_type fields only!"}), 400
