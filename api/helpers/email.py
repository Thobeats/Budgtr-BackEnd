#!/usr/bin/python3
"""Email Class"""

import smtplib, ssl
from dotenv import load_dotenv
from os import getenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    __port = None
    __password = None
    __email = None
    __host = None
    __server = None

    def __init__(self) -> None:
        """Creates the smtp client"""
        load_dotenv()

    def start_email_engine(self)->None:
        """Starts the Email COnnection"""
        try:
            self.__email = getenv('SMTP_EMAIL')
            self.__password = getenv('SMTP_PASSWORD')
            self.__port = getenv('SMTP_PORT')
            self.__host = getenv('SMTP_HOST')
            self.__server = smtplib.SMTP_SSL(self.__host, self.__port)
            self.__server.ehlo()            
            self.__server.login(self.__email, self.__password)
        except Exception as e:
            print(e)
            

    def send_email(self, receiver_email, message) -> None:
        """send an email to a user"""
        try:
            self.__server.sendmail('info@budgtr.com',receiver_email, message)
        except Exception as e:
            print(e)
