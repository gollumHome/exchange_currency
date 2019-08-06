from flask import Blueprint


ov = Blueprint("order",  __name__, url_prefix="/api/v1/order")

from . import maker_order_views
