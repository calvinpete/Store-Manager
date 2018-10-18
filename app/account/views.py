from flask import jsonify, request
from app import app
from app.accounts import staff


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"message": "Invalid entry"}), 400


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message": "This page does not exist"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"message": "This method is not allowed for the requested URL"}), 405


@app.route('/store-manager/api/v1/auth/signup', methods=['POST'])
def sign_up():
    data = request.get_json()
    if len(data.keys()) != 6:
        return jsonify({"message": "please type in the missing fields"}), 400

    name = data['name']
    company_id = data['company_id']
    phone_number = data['phone_number']
    username = data['username']
    email_address = data['email_address']
    password = data['password']

    if staff.check_input_type(
            name=name,
            company_id=company_id,
            phone_number=phone_number,
            email_address=email_address,
            username=username,
            password=password):
        return jsonify({"message": "Please a enter a string"})

    if staff.check_input_validity(
            name=name,
            company_id=company_id,
            phone_number=phone_number,
            email_address=email_address,
            username=username,
            password=password):
        return jsonify({"message": "Values are required"}), 400

    if not staff.validate_email_address(email_address):
        return jsonify({"message": "The email should follow the format of valid emails (johndoe@mail.com)"}), 400

    if staff.check_user(email_address):
        return jsonify({"message": "User already exists"}), 409
    else:
        staff.register(name, company_id, phone_number, email_address, username, password, admin=True)
        return jsonify({"message": "You've been successfully registered"}), 201
