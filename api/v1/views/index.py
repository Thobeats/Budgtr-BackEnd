#!/usr/bin/python3
"""
creates route /status for blueprint object app_views
"""

from api.v1.views import app_views, validator, httpresp, storage, email, otphelper
from models.user import User
from models.otp import Otp
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


@app_views.route("/send_mail", methods=['GET'],
                 strict_slashes=False)
def send_mail(toAddress, message)->None:
    """
    Send Email
    """
    try:
        email.send_email(toAddress, message)
        return jsonify({}), 200
    except Exception as e:
        print(e)

@app_views.route("/send_otp_mail", methods=['POST'],
                 strict_slashes=False)
def send_otp()->None:
    """send email otp to verify the email"""
    try:
        json_message = request.get_json()
        if "email" not in json_message or json_message['email'] is "":
            return httpresp.error({}, "Email not found", 404)
        user_email = json_message['email']
        otphelper.generate(5)
        new_otp = otphelper.get_otp(user_email, storage)
        otp_email_template = open('email_templates/otp.html').read()
        otp_email = otp_email_template.replace("[OTP]", str(new_otp))
        email.send_email(user_email, otp_email, 'html')
        return jsonify({}), 200
    except Exception as e:
        print(e)
        return httpresp.error({}, e, 404)