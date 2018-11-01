import jwt
import datetime
from functools import wraps
from flask import jsonify, request
from app.api.v1 import app
from app.api.v1.models.accounts import Account
from app.api.v1.validator import UserValidator
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


@app.route('/store-manager/api/v1/auth/login', methods=['POST'])
def login():

    try:

        data = request.get_json()
        if len(data.keys()) != 2:
            return jsonify({"message": "please make sure you have both "
                                       "the email_address field and password field only"}), 400

        email_address = data['email_address']
        password = data['password']

        validate = UserValidator(email_address, password)

        if Account.get_user_name(email_address) is None:
            return jsonify({"message": "User does not exist, please register"}), 400

        if not validate.check_password():
            return jsonify({"message": "wrong password, please try again"}), 400
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
    except KeyError:
        return jsonify({"message": "please make sure you have both "
                                   "the email_address field and password field only"}), 400


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
            current_user = Account.get_user_email_address(email_address=data["email_address"])
        except:
            return jsonify({"message": "Token is invalid"}), 401
        return f(current_user, *args, **kwargs)

    return decorated
