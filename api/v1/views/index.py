#!/usr/bin/python3
"""
creates route /status for blueprint object app_views
"""

from api.v1.views import app_views, validator, httpresp, storage
from models.user import User
from flask import abort, request, jsonify
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from api.helpers.httpresponses import HttpResponse
from flask_jwt_extended import create_access_token, JWTManager
from datetime import timedelta
import json

@app_views.route("/login", methods=['POST'],
                 strict_slashes=False)
def login():
    """
    Logs a user into the application
    """
    # validate the request
    
    try:
        validated = validator.make(request.get_json(), {
            "email" : ['required', 'email'],
            "password" : ['required', 'min:5', 'max:10']
        })

        # Check if the email exist in the system
        user = storage.get_user_by_email(validated['email'])

        if user is None:
            return httpresp.error({}, "Email not found, please check your email and try again", 404)
        else:
            # check the password
            check_password = user.check_password(validated['password'])
            if check_password:
                access_token = create_access_token(identity=validated['email'],
                                                   expires_delta=timedelta(hours=4))
                response = {
                    "access_token" : access_token,
                    "user" : user.to_dict()
                }

                return httpresp.success(response, "Login Success", 200)
            else:
                return httpresp.error({}, "Password is wrong, please check your password", 404)
    except ValidationError as ve:
        return jsonify({
            "code" : 1,
            "message" : ve.message
        })



@app_views.route("/register", methods=['POST'],
                 strict_slashes=False)
def user_register():
    """
    Registers a new user
    """
    try:
        validated = validator.make(request.get_json(), {
            "email" : ['required', 'email'],
            "password" : ['required', 'min:5', 'max:10']
        })

        newUser = User(email=validated['email'], password=validated['password'])
        response = newUser.save()
        if response:
            return httpresp.success({}, "Welcome to Budgtr, Registration Successful")
        else:
            return httpresp.error({}, "Registration failed, try again", 400)
    except ValidationError as ve:
        return jsonify({
            "code" : 1,
            "message" : ve.message
        })