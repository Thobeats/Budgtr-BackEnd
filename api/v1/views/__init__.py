"""
ALL API VIEWS
"""

from flask import Blueprint
from api.helpers.validator import Validator
from api.helpers.httpresponses import HttpResponse
from models import storage


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
validator = Validator()
httpresp = HttpResponse()

from api.v1.views.users import *
from api.v1.views.index import *