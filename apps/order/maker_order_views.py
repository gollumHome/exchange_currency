# -*- coding: utf-8 -*-
import enum
from decimal import Decimal
from .constant import TAKER_ORDER_STATUS,PROCESS_STATUS_EXPIRE_TIME
from apps import db
from flask import jsonify, request
import uuid
import logging
from apps.order import ov
from apps.order.db_submit_controller import AtoSubmit
from apps.order.order_controller import OrderApi
from apps.order.exchange_process_controller import ProcesApi
from apps.models import *

from apps.redis_client import RedisClient
from apps.models import *

order_api = OrderApi(db)
redis_client = RedisClient()

# create logger
logger = logging.getLogger(__name__)


@ov.route('/maker_order/', methods=['POST'])
def create_order():
    param_data = request.json
    user_id = 1
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

    result_order = order_api.create_maker_order(user_id, book_no, hold_currency,
                                    hold_amount, exchange_currency,
                                    exchange_amount, exchange_rate, status)

    # taker
    extend_remark = ''
    entrust_type = 1
    resultproces = ProcesApi.create_exchange_process(book_no, user_id, status,
                                                     extend_remark, entrust_type)

    if result_order and resultproces:
        return
    else:
        return jsonify({})


@ov.route('/maker_order/', methods=['GET'])
def get_order_info():
    pk = request.args.get('pk')
    obj = order_api.get_maker_order_by_pk(pk)
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


@ov.route('/maker_order/', methods=['PUT'])
def update_maker_order():
    pk = request.args.get('pk')
    status = request.args.get('status')
    if status == TAKER_ORDER_STATUS['set_wallet']:
        key = ''
        expired_time = PROCESS_STATUS_EXPIRE_TIME['set_wallet']
        motior_result = redis_client.add_monitor_porcess_order(key,
                                                               expired_time)
        if not motior_result:
            return jsonify({'code': '500', 'info': "system err"})
        obj = TakerOrder.query.filter_by(id=pk).first()
        if obj:
            with AtoSubmit(db) as submit_message:
                related_maker_order = OrderApi. \
                    update_taker_related_maker_order(obj.book_no, status)
                related_process = ProcesApi.update_taker_related_porcess(obj.book_no, status)
                if not related_maker_order and not related_process:
                    return jsonify({'code': '500', 'info': "update order or process err"})
                result = OrderApi.update_taker_order(pk, status)
                logger.info('update taker order message %s', submit_message)
                if not result:
                    return jsonify({'code': '500', 'info': "system err"})

    if status == TAKER_ORDER_STATUS['sended']:
        result = OrderApi.update_taker_order(pk, status)
        if not result:
            return jsonify({'code': '500', 'info': "system err"})
    if status == TAKER_ORDER_STATUS['received']:
        result = OrderApi.update_taker_order(pk, status)
        if not result:
            return jsonify({'code': '500', 'info': "system err"})
    if status == TAKER_ORDER_STATUS['disputed']:
        result = OrderApi.update_taker_order(pk, status)
        if not result:
            return jsonify({'code': '500', 'info': "system err"})
    if status == TAKER_ORDER_STATUS['complete']:
        result = OrderApi.update_taker_order(pk, status)
        if not result:
            return jsonify({'code': '500', 'info': "system err"})
    if status == TAKER_ORDER_STATUS['canceled']:
        result = OrderApi.update_taker_order(pk, status)
        if not result:
            return jsonify({'code': '500', 'info': "system err"})
    view_data = dict()
    view_data['code'] = '200'
    view_data['data'] = {}
    return jsonify(view_data)

