#!/usr/bin/python3
"""
Budgtr API
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from dotenv import load_dotenv
from os import getenv
from flask_jwt_extended import JWTManager


load_dotenv()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET')
jwt = JWTManager(app)
app.register_blueprint(app_views)


@app.route('/', strict_slashes=False)
def index():
    """returns Hello HBNB!"""
    return jsonify({
        "success" : "Welcome to Budgtr",
        "code" : 200
    }), 200

@app.errorhandler(404)
def not_found(e):
    """Handler for the 404 error"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
