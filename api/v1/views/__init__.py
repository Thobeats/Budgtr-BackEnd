"""
ALL API VIEWS
"""

from flask import Blueprint
from api.helpers.validator import Validator
from api.helpers.httpresponses import HttpResponse
from api.helpers.email import Email
from api.helpers.otphelper import OtpHelper
from models import storage


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
validator = Validator()
httpresp = HttpResponse()
email = Email()
otphelper = OtpHelper()
email.start_email_engine()
otphelper.start_otp_engine()

from api.v1.views.users import *
from api.v1.views.index import *