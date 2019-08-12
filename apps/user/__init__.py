from flask import Blueprint


uv = Blueprint("user",  __name__, url_prefix="/api/v1/user")

from . import views

