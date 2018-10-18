from flask import jsonify, request
from app import app
from app.accounts import staff


@app.errorhandler(400)
def bad_request():
    return jsonify({"message": "Invalid entry"}), 400


@app.errorhandler(404)
def page_not_found():
    return jsonify({"message": "This page does not exist"}), 404


@app.errorhandler(405)
def method_not_allowed():
    return jsonify({"message": "This method is not allowed for the requested URL"}), 405


