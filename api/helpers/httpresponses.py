#!/usr/bin/python3
"""

HttpResponse
200 - OK
400 - BAD REQUEST
404 - NOT FOUND
500 - SERVER ERROR
"""

from flask import jsonify


class HttpResponse:
    """HttpResponse is a class of all API responses"""

    def success(self, data, message, status_code=200):
        """returns the success response"""
        response = {
            "code" : 0,
            "message" : message,
            "status_code" : status_code,
            "data" : data
        }

        return jsonify(response)
    
    def error(self, data, message, status_code):
        """returns the error response"""
        response = {
            "code" : 1,
            "message" : message,
            "status_code" : status_code,
            "data" : data
        }

        return jsonify(response)
