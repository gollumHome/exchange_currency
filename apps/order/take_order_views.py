# -*- coding: utf-8 -*-

from .constant import TAKER_ORDER_STATUS,\
    PROCESS_STATUS_EXPIRE_TIME, ENTRUST_TYPE,\
    EXCHANGE_PROCESS_STATUS
from flask import jsonify, request
import uuid
import logging
from apps.order import ov

from apps.order.order_controller import OrderApi
from apps.order.exchange_process_controller import ProcesApi
from apps.order.db_submit_controller import AtoSubmit
from apps.order.subscribe_controller import SubscribeApi
from apps.tencent_sms import TencentSms

from apps.redis_client import RedisClient
from apps.models import *

order_api = OrderApi(db)
process_api = ProcesApi(db)
scribe_api = SubscribeApi(db)
redis_client = RedisClient()
sms_api = TencentSms()

# create logger
logger = logging.getLogger(__name__)


@ov.route('/taker_order/', methods=['POST'])
def create_taker_order():
    param_data = request.json
    #user_id = request.cookies.get('user_id')
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
                                                 exchange_currency)
    book_no = str(uuid.uuid1())
    order_status = TAKER_ORDER_STATUS['matched']
    entrust_type = ENTRUST_TYPE['taker']

    with AtoSubmit(db):
        # create taker order
        result_taker = order_api.create_taker_order(user_id, book_no, hold_currency,
                                                    hold_amount, exchange_currency,
                                                    exchange_amount, exchange_rate, order_status)

        # create taker porcess,set expire time
        exprocess_status = EXCHANGE_PROCESS_STATUS['matched']
        resultproces = process_api.create_exchange_process(book_no, user_id,
                                                         exprocess_status,
                                                         entrust_type)
    view_data = dict()
    if result_taker and resultproces:
        view_data['code'] = '200'
        view_data['data'] = {}
    else:
        view_data['code'] = '500'
        view_data['info'] = 'system err'
    return jsonify(view_data)


@ov.route('/taker_order/', methods=['PUT'])
def update_taker_order():
    pk = request.args.get('pk')
    param_data = request.json
    extend_remark = param_data.get('extend_remark', "")
    status = param_data.get('status', "")

    if not extend_remark and not status:
        return jsonify({"code": "400", "info": "缺少关键参数"})

    obj = TakerOrder.query.filter_by(id=pk).first()
    if not obj:
        return jsonify({'code': '500', 'info': "system err"})
    process = ExchangeProgres.query.filter(book_no=obj.book_no,
                                           entrust_type=ENTRUST_TYPE['taker']).first()
    if not process:
        return jsonify({'code': '500', 'info': "system err"})

    if status == TAKER_ORDER_STATUS['matched']:
        with AtoSubmit(db):
            order_api.update_taker_related_maker_order(obj.book_no, status)
            process_api.update_taker_related_porcess(obj.book_no, ENTRUST_TYPE['2'], status)
            order_api.update_taker_order(pk, status)

        scribe_result = scribe_api.subscribe_process_exchange(process.id,
                                                              process.book_no,
                                                              EXCHANGE_PROCESS_STATUS['matched'])
        if not scribe_result:
            return jsonify({'code': '500', 'info': "system err"})

        # when taker the order , then notice to maker order is matched
        sms_result = sms_api.send_single('1874566734221', 'your order is mathed')
        logger.info('semd message %s to user  %s', sms_result)


    if status == TAKER_ORDER_STATUS['set_wallet']:
        if obj:
            with AtoSubmit(db) as submit_message:
                order_api.update_taker_order(pk, status)
                process_obj = ProcesApi.get_exchange_process_obj(obj.book_no, 'taker')
                ProcesApi.add_exchange_wallet(process_obj.id, extend_remark)
                SubscribeApi.subscribe_process_exchange(pk=process_obj.id,
                                                        book_no=process_obj.book_no,
                                                        status=EXCHANGE_PROCESS_STATUS['set_wallet'])

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

