#!/usr/bin/python3
"""OtpHelper Class"""

from random import randint
from uuid import uuid4
from models.otp import Otp

class OtpHelper:
    """The OtpHelper class send otps to the user's email"""
    __otp = None
    __db = None
    __otpinstance = None

    def __init__(self, length=5):
        """Initialises a new Otp Instance"""
        

    def start_otp_engine(self):
        self.__otpinstance = Otp()

    def generate(self, length=5):
        """generates a random otp"""
        start = pow(10, length)
        end = pow(10, length + 1) - 1
        self.__otp = randint(start, end)

    def get_otp(self, identifier, dbinstance):
        """return the otp to the user"""
        self.__otpinstance.identifier = identifier
        self.__otpinstance.otp_code = self.__otp
        self.__otpinstance.id = uuid4()
        dbinstance.new(self.__otpinstance)
        dbinstance.save()
        return(self.__otp)
