from flask import Blueprint


ov = Blueprint("order",  __name__, url_prefix="/api/v1/order")

from apps.order.views import maker_order_views, take_order_views, upload_proof_views, exchage_fee_views

