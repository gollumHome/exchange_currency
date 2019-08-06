# -*- coding: utf-8 -*-
import enum
from decimal import Decimal
from apps import db
from flask import jsonify, request
import uuid
import logging
from apps.order import ov

from apps.order.order_controller import OrderApi
from apps.models import *

order_api = OrderApi(db)

# create logger
logger = logging.getLogger(__name__)


@ov.route('/taker_order/', methods=['POST'])
def create_order():
    param_data = request.json
    #user_id = request.cookies.get('user_id')
    user_id = 001
    exchange_rate = OrderApi.get_current_exchange_rate()
    hold_currency = param_data.get('hold_currency', '')
    hold_amount = param_data.get('hold_amount', '')
    exchange_currency = param_data.get('exchange_currency', '')
    if hold_currency == '' or hold_amount == '' \
            or exchange_currency == '':
        return jsonify({"code": "400", "info": "缺少关键参数"})
    exchange_amount = OrderApi.currency_exchange(hold_currency,
                                                 hold_amount,
                                                 exchange_currency)
    book_no = str(uuid.uuid1())
    user_id = user_id
    exchange_amount = exchange_amount
    exchange_rate = exchange_rate
    status = '1'
    request.data['user_id'] = user_id
    request.data['exchange_amount'] = exchange_amount
    request.data['exchange_rate'] = exchange_rate
    request.data['status'] = '1'

    result = order_api.create_taker_order(user_id, book_no, hold_currency,
                                    hold_amount, exchange_currency,
                                    exchange_amount, exchange_rate, status)

    return jsonify(result)




