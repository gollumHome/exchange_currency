# -*- coding: utf-8 -*-

from .constant import TAKER_ORDER_STATUS, \
    ENTRUST_TYPE,\
    EXCHANGE_PROCESS_STATUS,MAKER_ORDER_STATUS
from flask import jsonify, request
import uuid
import logging
from apps.order import ov

from apps.order.order_controller import OrderApi
from apps.order.exchange_process_controller import ProcesApi
from apps.order.db_submit_controller import AtoSubmit
from apps.order.subscribe_controller import SubscribeApi
from apps.order.sms_controller import SmsController

from apps.models import *

order_api = OrderApi(db)
process_api = ProcesApi(db)
scribe_api = SubscribeApi(db)

sms_api = SmsController()

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
    """【更新taker order 状态】
             url格式： /api/v1/order/taker_order/?pk=4
            @@@
            #### args

            | args | nullable | type | remark |
            |--------|--------|--------|--------|
            |    hold_currency    |    false    |    string   |    手机号  |
            | exchange_currency  |    false    |    string   |            |
            |   hold_amount    |    false    |    string   |    手机号  |
            |   exchange_amount    |    false    |    string   |    手机号  |
            |   book_no    |    false    |    string   |    手机号  |
            |  status    |    false    |    string   |    手机号  |
            #### return
            - ##### json
            >  {"code": "200"}
            @@@
            """
    pk = request.args.get('pk')
    status = request.args.get('status')

    if not status and not pk:
        return jsonify({"code": "400", "info": "缺少关键参数"})

    obj = TakerOrder.query.filter_by(id=pk).first()
    if not obj:
        return jsonify({'code': '500', 'info': "内部错误，读取吃单失败"})

    process = ExchangeProgres.query.filter(ExchangeProgres.book_no == obj.book_no,
                                           ExchangeProgres.entrust_type == 'taker').first()
    if not process:
        return jsonify({'code': '500', 'info': "内部错误，读取交易数据失败"})

    if status == TAKER_ORDER_STATUS['matched']:
        transaction = update_taker_order_transtions('matched', pk, obj.book_no,
                                      MAKER_ORDER_STATUS['matched'],
                                      TAKER_ORDER_STATUS['matched'],
                                      EXCHANGE_PROCESS_STATUS['matched'],
                                      ENTRUST_TYPE['taker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "吃单内部错误"})
        scribe_result = scribe_api.subscribe_process_exchange(process.id,
                                                              process.book_no,
                                                              EXCHANGE_PROCESS_STATUS['matched'])
        if not scribe_result:
            return jsonify({'code': '500', 'info': "设置吃单超时过程失败"})
        # when taker the order , then notice to maker order is matched,book_no Only one
        sms_result = sms_api.send_2maker_matched(obj.book_no)
        logger.info('semd message %s to user  %s', sms_result)
        if not sms_result:
            return jsonify({'code': '500', 'info': "通知创单匹配信息失败"})

    if status == TAKER_ORDER_STATUS['set_wallet']:
        extend_remark = request.args.get('extend_remark', "")
        if not extend_remark:
            return jsonify({"code": "400", "info": "缺少关键参数"})
        transaction = update_taker_order_transtions('set_wallet',pk, obj.book_no,
                                      MAKER_ORDER_STATUS['set_wallet'],
                                      TAKER_ORDER_STATUS['set_wallet'],
                                      EXCHANGE_PROCESS_STATUS['set_wallet'],
                                      ENTRUST_TYPE['taker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "吃单添加钱包内部错误"})

        process_obj = process_api.get_exchange_process_obj(obj.book_no,
                                                         ENTRUST_TYPE['taker'])
        if not process_obj:
            return jsonify({'code': '500', 'info': "获取交易对象失败"})
        set_wallet_status = process_api.add_exchange_wallet(process_obj.id, extend_remark)
        if not set_wallet_status:
            return jsonify({'code': '500', 'info': "添加钱包失败，重新添加"})
        scribe_result = scribe_api.subscribe_process_exchange(process.id,
                                                              process.book_no,
                                                              EXCHANGE_PROCESS_STATUS['set_wallet'])
        if not scribe_result:
            logger.info("add taker order = %s wallet err %s",obj.book_no,scribe_result)
            return jsonify({'code': '500', 'info': "添加钱包过程失败"})

    if status == TAKER_ORDER_STATUS['sended']:
        transaction = update_taker_order_transtions('sended',pk, obj.book_no,
                                      MAKER_ORDER_STATUS['sended'],
                                      TAKER_ORDER_STATUS['sended'],
                                      EXCHANGE_PROCESS_STATUS['sended'],
                                      ENTRUST_TYPE['taker'])

        if not transaction:
            return jsonify({'code': '500', 'info': "吃单设置sended状态内部错误"})
        scribe_result = scribe_api.subscribe_process_exchange(process.id,
                                                              process.book_no,
                                                              EXCHANGE_PROCESS_STATUS['set_wallet'])
        if not scribe_result:
            return jsonify({'code': '500', 'info': "订阅吃单sended状态超时时间失败"})

    if status == TAKER_ORDER_STATUS['received']:
        transaction = update_taker_order_transtions('received',pk, obj.book_no,
                                      MAKER_ORDER_STATUS['received'],
                                      TAKER_ORDER_STATUS['received'],
                                      EXCHANGE_PROCESS_STATUS['received'],
                                      ENTRUST_TYPE['taker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "吃单设置received状态内部错误"})
    if status == TAKER_ORDER_STATUS['disputed']:
        transaction = update_taker_order_transtions('disputed',pk, obj.book_no,
                                      MAKER_ORDER_STATUS['received'],
                                      TAKER_ORDER_STATUS['received'],
                                      EXCHANGE_PROCESS_STATUS['received'],
                                      ENTRUST_TYPE['taker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "吃单设置disputed状态内部错误"})
        scribe_result = scribe_api.subscribe_process_exchange(process.id,
                                                              process.book_no,
                                                              EXCHANGE_PROCESS_STATUS['set_wallet'])
        if not scribe_result:
            return jsonify({'code': '500', 'info': "订阅吃单申诉状态超时时间失败"})
    if status == TAKER_ORDER_STATUS['complete']:
        transaction = update_taker_order_transtions('complete',pk, obj.book_no,
                                      MAKER_ORDER_STATUS['complete'],
                                      TAKER_ORDER_STATUS['complete'],
                                      EXCHANGE_PROCESS_STATUS['complete'],
                                      ENTRUST_TYPE['taker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "吃单设置complete状态内部错误"})
    if status == TAKER_ORDER_STATUS['canceled']:
        transaction = update_taker_order_transtions('canceled',pk, obj.book_no,
                                      MAKER_ORDER_STATUS['canceled'],
                                      TAKER_ORDER_STATUS['canceled'],
                                      EXCHANGE_PROCESS_STATUS['canceled'],
                                      ENTRUST_TYPE['taker'])
        if not transaction:
            return jsonify({'code': '500', 'info': "吃单设置canceled状态内部错误"})
    view_data = dict()
    view_data['code'] = '200'
    view_data['info'] = ''
    view_data['data'] = {}
    return jsonify(view_data)


def update_taker_order_transtions(type, pk, book_no, maker_status,
                                  taker_status, process_status,
                                  process_entrust_type):

    try:
        with AtoSubmit(db):
            if type == 'canceled' or 'disputed':
                process_api.update_taker_related_porcess(book_no, process_entrust_type, process_status)
                order_api.update_taker_order(pk, taker_status)

            else:
                order_api.update_taker_related_maker_order(book_no, maker_status)
                process_api.update_taker_related_porcess(book_no, process_entrust_type, process_status)
                order_api.update_taker_order(pk, taker_status)
        return True
    except Exception:
        return False





