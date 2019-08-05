# -*- coding: utf-8 -*-

import time
import json
from decimal import Decimal
from traceback import print_exc
from flask import g,jsonify, current_app, request
import logging
from apps.order import ov

from apps.OrderService import OrderApi
from apps.common import identify_required
from apps.models import *

order_api = OrderApi(db)

# create logger
logger = logging.getLogger(__name__)


@ov.route('/order', methods=['POST'])
def create_order():
    """创建订单
                @@@
                #### args

                | args | nullable | type | remark |
                |--------|--------|--------|--------|
                |   user_id    |    false    |    int   |    创建订单用户id  |
                |   enroll_id    |    true    |    int   |    报名记录id (开通会员时为空)  |
                |    merchant_id    |    false    |    int   |    商家ID |
                |    product_id    |    false    |    int   |    产品id (activity_id 或者course_id或者套餐id)  |
                |    title    |    false    |    string   |    活动课程名称或者会员套餐名称   |
                |    shares    |    false    |    string   |    商品数 (默认为1)  |
                |    img_url    |    true    |    string   |    图片地址 （开通会员时,不用传参 ） |
                |    price    |    false    |    string   |    交易价格   |
                |    order_amount    |    false    |    string   |    订单金额   |
                |    attach    |    false   |    json   |    开通会员时的附加信息 {"member_type":"gold","package_title":"黄金会员5年套餐","use_time":5}   购买课程时的附加值 {"course_type":"normal/experience"}|
                |    order_type    |    false    |    string   |    订单类型 ('activity','member','course')  |

                #### return
                - ##### json
                >  {"code": "success","data": {"appid" :"44444idjuej","mch_id" :"44444idjuej","nonce_str" :"44444idjuej",
                "package" :"prepay_id=wx2017033010242291fcfe0db70013231072","signType":"MD5","timeStamp" :14678909,"pay_sign":"22D9B4E54AB1950F51E0649E8810ACD6"}
                @@@
     """

    json_data: dict = request.json
    user_id = json_data.get('user_id', None)
    enroll_id = json_data.get('enroll_id', None)
    order_type = json_data.get('order_type', None)
    merchant_id = json_data.get('merchant_id', None)
    product_id = json_data.get('product_id', None)
    title = json_data.get('title', None)
    shares = json_data.get('shares', 1)
    img_url = json_data.get('img_url', None)
    price = json_data.get('price', 0)
    order_amount = json_data.get('order_amount', 0)
    attach = json_data.get('attach', {})
    attach = eval(str(attach))

    if order_type is None or user_id is None or product_id is None:
        return jsonify({"code": "error", "info": "缺少关键参数"})

    order_amount = Decimal(order_amount).quantize(Decimal('0.0'))
    result = order_api.create_order(int(user_id), int(merchant_id), int(product_id),
                                    title, int(shares), img_url, int(price), int(order_amount),
                                    attach, order_type,enroll_id)
    return jsonify(result)


@ov.route('/order/<order_no>', methods=['GET'])
def get_order_info(order_no):
    """查询指定订单号订单
            @@@
            #### args

            | args | nullable | type | remark |
            |--------|--------|--------|--------|
            |  order_no    |    false    |    string   |    订单号   |
            |    order_type    |    false    |    string   |    订单类型 ('activity','member','course')  |

            #### return
            - ##### json
            > {"code": "success", "data": {"id": 1, "order_no": "8j38jdlmbafgbtykyyvflgws88", "product_id": 1, "merchant_id": 1, "user_id": 2, "product_num": 2, "price": 460, "img_url":"6hdymmcaabagcc.png","order_amount": 4500, "status": "payed", "finish_time": 1567890000, "create_time": 1567890666}}
            @@@
    """
    order_type = request.args.get('order_type',None)
    t = order_api.get_order_by_no(order_no,order_type)
    if order_type == 'member':
        order = {"id": t.id, "order_no": t.order_no, "title": t.title, "product_id": t.product_id,
                 "merchant_id": t.merchant_id, "user_id": t.user_id, "shares": t.shares,
                 "price": t.price, "img_url": t.img_url, "order_amount": t.order_amount, "status": t.status,
                 "organization_name": t.organization_name,"telephone": t.telephone, "finish_time": t.finish_time, "create_time": t.create_time} if t else None
    else:
        order = {"id": t.id, "order_no": t.order_no, "title": t.title, "product_id": t.product_id,
                 "merchant_id": t.merchant_id, "user_id": t.user_id, "shares": t.shares,
                 "price": t.price, "img_url": t.img_url, "order_amount": t.order_amount, "status": t.status,
                 "nickname": t.nickname,"head_url": t.head_url, "finish_time": t.finish_time, "create_time": t.create_time} if t else None

    view_data = dict()
    view_data['code'] = 'success'
    view_data['data'] = order

    return jsonify(view_data)

