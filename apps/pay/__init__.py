from flask import Blueprint


pv = Blueprint("pay",  __name__, url_prefix="/api")

from . import views
