#!/usr/bin/python3
"""A Validator Class"""

from jsonschema.exceptions import ValidationError
import re

class Validator:

    def __init__(self) -> None:
        self.__errors = dict()

    def make(self, fields, rules):
        self.__errors = dict()
        """creates a new validation request"""
        for key, value in rules.items():
            for val in value:
                # check if val has ':'
                if ":" in val:
                    vals = val.rsplit(":")
                    self.call_functions()[vals[0]](fields, key, vals[1])
                else:
                    self.call_functions()[val](fields, key)
        if len(self.__errors) > 0:
            raise ValidationError(self.__errors)
        else:
            return fields
                
    def call_functions(self):
        map = {
            "required" : self.is_required,
            "email" : self.is_email,
            "min" : self.is_min,
            "max" : self.is_max
        }
        return map


    def is_required(self, fields, key)->None:
        """Validates if a field is required"""
        value = fields[key]
        if value is None or value == '':
            error = "The {} field is required".format(key)
            self.__logError(key, error)
        
    def is_email(self, fields, key)->None:
        """checks if the field is a valid email"""
        value = fields[key]
        check = re.fullmatch("^[a-zA-Z0-9_.±]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$", value)
        if not check:
            error = "This is an invalid email"
            self.__logError(key, error)

    def is_min(self, fields, key, min=3):
        """check the min length of the value"""
        value = fields[key]
        if len(value) < int(min):
            error = "The {} length should not be less than {}".format(key, min)
            self.__logError(key, error)


    def is_max(self, fields, key, max=20):
        """check the max length of the value"""
        value = fields[key]
        if len(value) > int(max):
            error = "The {} length should not be more than {}".format(key, max)
            self.__logError(key, error)
        
    def __logError(self, key, error):
        """logs the validation errors"""
        if key in self.__errors:
            self.__errors[key].append(error)
        else:
            self.__errors[key] = []
            self.__errors[key].append(error)

