# -*- coding: utf-8 -*-
import enum
from decimal import Decimal
from flask import jsonify, request
import uuid
import logging
from apps.order import ov

from apps.order.order_controller import OrderApi
from apps.models import *

order_api = OrderApi(db)

# create logger
logger = logging.getLogger(__name__)


@ov.route('/maker_order/', methods=['POST'])
def create_order():
    param_data = request.json
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
                                                 exchange_currency,
                                                 exchange_rate)
    book_no = str(uuid.uuid1())
    user_id = user_id
    exchange_amount = exchange_amount
    exchange_rate = exchange_rate
    status = '1'

    result = order_api.create_maker_order(user_id, book_no, hold_currency,
                                    hold_amount, exchange_currency,
                                    exchange_amount, exchange_rate, status)
    return jsonify(result)


@ov.route('/maker_order/', methods=['GET'])
def get_order_info():
    pk = request.args.get('pk')
    obj = order_api.get_order_by_pk(pk)
    if obj:
        resp_data = {"id": obj.id,
                     "book_no": obj.book_no,
                     "user_id": obj.user_id,
                     "hold_currency": obj.hold_currency,
                     "exchange_currency": obj.exchange_currency,
                     "hold_amount": obj.hold_amount,
                     "exchange_amount": obj.exchange_amount,
                     "exchange_rate": obj.exchange_rate,
                     "create_time": obj.create_time,
                     "status": obj.status
                     }
    else:
        resp_data = {}
    view_data = dict()
    view_data['code'] = '200'
    view_data['data'] = resp_data
    return jsonify(view_data)

