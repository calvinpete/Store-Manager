import jwt
import datetime
from functools import wraps
from flask import jsonify, request
from app import app
from app.accounts import staff
from instance.config import Config


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
        return jsonify({"message": "Please a enter a string"}), 400

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


@app.route('/store-manager/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if len(data.keys()) != 2:
        return jsonify({"message": "please type in the missing fields"}), 400

    email_address = data['email_address']
    password = data['password']

    if not staff.check_user(email_address):
        return jsonify({"message": "User does not exist, please register"}), 400

    if not staff.check_password(password):
        return jsonify({"message": "Invalid password, please try again"}), 400
    else:
        token = jwt.encode(
            {
                "email_address": email_address,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            Config.SECRET_KEY
        )
        return jsonify(
            {
                "token": token.decode("UTF-8"),
                "message": "You have successfully logged in"
            }
        ), 200


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = staff.get_user(email_address=data["email_address"])
        except:
            return jsonify({"message": "Token is invalid"}), 401
        return f(current_user, *args, **kwargs)

    return decorated

