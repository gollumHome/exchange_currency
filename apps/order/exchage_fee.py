# -*- coding: utf-8 -*-
import enum
from decimal import Decimal
from .constant import TAKER_ORDER_STATUS,\
    PROCESS_STATUS_EXPIRE_TIME, ENTRUST_TYPE,\
    EXCHANGE_PROCESS_STATUS
from apps import db
from flask import jsonify, request
import uuid
import logging
from apps.order import ov

from apps.order.order_controller import OrderApi
from apps.models import *
from apps.tencent_sms import TencentSms

from apps.redis_client import RedisClient
from apps.models import *

order_api = OrderApi(db)
redis_client = RedisClient()
sms_api = TencentSms()

# create logger
logger = logging.getLogger(__name__)


@ov.route('/taker_order/fee', methods=['GET'])
def taker_order_exchange():
    pk = request.args.get('pk')
    obj = TakerOrder.query.filter(id=pk).first()
    if obj:
        return obj.exchange_amount ** 0.08
