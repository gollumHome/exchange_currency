# -*- coding: utf-8 -*-
import enum
from decimal import Decimal
from .constant import TAKER_ORDER_STATUS,MAKER_ORDER_STATUS\
    ,EXCHANGE_PROCESS_STATUS,ENTRUST_TYPE

from flask import jsonify, request
import uuid
import logging
from apps.order import ov
from apps.order.db_submit_controller import AtoSubmit
from apps.order.order_controller import OrderApi
from apps.order.exchange_process_controller import ProcesApi
from apps.order.subscribe_controller import SubscribeApi
from apps.order.sms_controller import SmsController
from apps.models import *

from apps.redis_client import RedisClient
from apps.models import *

order_api = OrderApi(db)
redis_client = RedisClient()
scribe_api = SubscribeApi(db)
process_api = ProcesApi(db)
sms_api = SmsController()
# create logger
logger = logging.getLogger(__name__)


@ov.route('/maker_order/', methods=['POST'])
def create_order():
    """

    :return:
    """
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
                                                 exchange_currency)
    book_no = str(uuid.uuid1())
    status = MAKER_ORDER_STATUS['createded']

    with AtoSubmit(db):
        result_order_pk = order_api.create_maker_order(user_id, book_no, hold_currency,
                                        hold_amount, exchange_currency,
                                        exchange_amount, exchange_rate, status)

        # create taker porcess,set expire time
        # exprocess_status = EXCHANGE_PROCESS_STATUS['matched']
        # resultproces = process_api.create_exchange_process(book_no, user_id,
        #                                                    exprocess_status,
        #                                                    entrust_type)

    # taker
    # extend_remark = ''
    # entrust_type = 1
    # resultproces = ProcesApi.create_exchange_process(book_no, user_id, status,
    #                                                  extend_remark, entrust_type)

    view_data = dict()
    if result_order_pk:
        view_data['code'] = '200'
        view_data['data'] = {"id": result_order_pk}
    else:
        view_data['code'] = '500'
        view_data['info'] = '内部错误'
    return jsonify(view_data)


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

    if not pk and not status:
        return jsonify({'code': '400', 'info': "参数错误"})

    obj = MakerOrder.query.filter_by(id=pk).first()
    if not obj:
        return jsonify({'code': '500', 'info': "读取创单Obj 错误"})

    if status == TAKER_ORDER_STATUS['set_wallet']:
        extend_remark = request.args.get('extend_remark', "")
        if not extend_remark:
            return jsonify({"code": "400", "info": "缺少关键参数"})
        transaction = update_maker_order_transtions( pk, obj.book_no,
                                                    MAKER_ORDER_STATUS['set_wallet'],
                                                    EXCHANGE_PROCESS_STATUS['set_wallet'],
                                                    ENTRUST_TYPE['maker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "挂单内部错误"})
        process_obj = process_api.get_exchange_process_obj(obj.book_no,
                                                           ENTRUST_TYPE['maker'])
        if not process_obj:
            jsonify({'code': '500', 'info': "获取交易对象失败"})
        set_wallet_status = process_api.add_exchange_wallet(process_obj.id, extend_remark)
        if not set_wallet_status:
            return jsonify({'code': '500', 'info': "添加钱包失败，重新添加"})
        scribe_result = scribe_api.subscribe_process_exchange(process_obj.id,
                                                              process_obj.book_no,
                                                              EXCHANGE_PROCESS_STATUS['set_wallet'])
        if not scribe_result:
            return jsonify({'code': '500', 'info': "设置挂单超时过程失败"})

    if status == TAKER_ORDER_STATUS['sended']:
        transaction = update_maker_order_transtions(pk, obj.book_no,
                                                    MAKER_ORDER_STATUS['sended'],
                                                    EXCHANGE_PROCESS_STATUS['sended'],
                                                    ENTRUST_TYPE['maker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "挂单内部错误"})
        process_obj = process_api.get_exchange_process_obj(obj.book_no,
                                                           ENTRUST_TYPE['maker'])
        if not process_obj:
            jsonify({'code': '500', 'info': "获取交易对象失败"})
        scribe_result = scribe_api.subscribe_process_exchange(process_obj.id,
                                                              process_obj.book_no,
                                                              EXCHANGE_PROCESS_STATUS['sended'])
        if not scribe_result:
            return jsonify({'code': '500', 'info': "设置挂单超时过程失败"})
    if status == TAKER_ORDER_STATUS['received']:
        transaction = update_maker_order_transtions(pk, obj.book_no,
                                                    MAKER_ORDER_STATUS['received'],
                                                    EXCHANGE_PROCESS_STATUS['received'],
                                                    ENTRUST_TYPE['maker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "挂单内部错误"})
        process_obj = process_api.get_exchange_process_obj(obj.book_no,
                                                           ENTRUST_TYPE['maker'])
        if not process_obj:
            jsonify({'code': '500', 'info': "获取交易对象失败"})
    if status == TAKER_ORDER_STATUS['disputed']:
        transaction = update_maker_order_transtions(pk, obj.book_no,
                                                    MAKER_ORDER_STATUS['disputed'],
                                                    EXCHANGE_PROCESS_STATUS['disputed'],
                                                    ENTRUST_TYPE['maker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "挂单内部错误"})
        process_obj = process_api.get_exchange_process_obj(obj.book_no,
                                                           ENTRUST_TYPE['maker'])
        if not process_obj:
            jsonify({'code': '500', 'info': "获取交易对象失败"})
        scribe_result = scribe_api.subscribe_process_exchange(process_obj.id,
                                                              process_obj.book_no,
                                                              EXCHANGE_PROCESS_STATUS['disputed'])
        if not scribe_result:
            return jsonify({'code': '500', 'info': "设置挂单超时过程失败"})
        sms_result = sms_api.send_both_disputed_info(obj.book_no)
        logger.info('semd message %s to user  %s', sms_result)
        if not sms_result:
            return jsonify({'code': '500', 'info': "通知创单申诉信息失败"})

    if status == TAKER_ORDER_STATUS['complete']:
        transaction = update_maker_order_transtions(pk, obj.book_no,
                                                    MAKER_ORDER_STATUS['complete'],
                                                    EXCHANGE_PROCESS_STATUS['complete'],
                                                    ENTRUST_TYPE['maker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "挂单内部错误"})
        process_obj = process_api.get_exchange_process_obj(obj.book_no,
                                                           ENTRUST_TYPE['maker'])
        if not process_obj:
            jsonify({'code': '500', 'info': "获取交易对象失败"})
        scribe_result = scribe_api.subscribe_process_exchange(process_obj.id,
                                                              process_obj.book_no,
                                                              EXCHANGE_PROCESS_STATUS['complete'])
        if not scribe_result:
            return jsonify({'code': '500', 'info': "设置挂单超时过程失败"})
    if status == TAKER_ORDER_STATUS['canceled']:
        transaction = update_maker_order_transtions(pk, obj.book_no,
                                                    MAKER_ORDER_STATUS['canceled'],
                                                    EXCHANGE_PROCESS_STATUS['canceled'],
                                                    ENTRUST_TYPE['maker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "挂单内部错误"})
        process_obj = process_api.get_exchange_process_obj(obj.book_no,
                                                           ENTRUST_TYPE['maker'])
        if not process_obj:
            jsonify({'code': '500', 'info': "获取交易对象失败"})
        scribe_result = scribe_api.subscribe_process_exchange(process_obj.id,
                                                              process_obj.book_no,
                                                              EXCHANGE_PROCESS_STATUS['canceled'])
        if not scribe_result:
            return jsonify({'code': '500', 'info': "设置挂单超时过程失败"})
    view_data = dict()
    view_data['code'] = '200'
    view_data['data'] = {}
    return jsonify(view_data)


def update_maker_order_transtions(type,pk, book_no,
                                  maker_status,
                                  process_status,
                                  process_entrust_type):

    try:
        with AtoSubmit(db):
            if type == 'disputed':
                order_api.update_maker_related_taker_order(book_no, maker_status)
                process_api.update_maker_related_porcess(book_no, process_entrust_type, process_status)
                order_api.update_maker_order(pk, maker_status)
            else:
                order_api.update_maker_order(pk, maker_status)
                process_api.update_maker_related_porcess(book_no, process_entrust_type, process_status)
        return True
    except Exception:
        return False