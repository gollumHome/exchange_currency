from flask import Blueprint


ov = Blueprint("order",  __name__, url_prefix="/api")

from . import views
