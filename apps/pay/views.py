# -*- coding: utf-8 -*-

import time
import json
from decimal import Decimal
from traceback import print_exc

import datetime
from flask import g,jsonify, current_app, request
import logging
from apps.pay import pv

from apps.PayService import PayApi
from apps.order.order_controller import OrderApi
from apps.utils import Utils
from apps.models import *
from celerys import tasks
from apps.common import identify_required

pay_api = PayApi(db)
order_api = OrderApi(db)

# create logger
logger = logging.getLogger(__name__)


@pv.route("/")
def hello():
    return jsonify({"message": "Hello, pay!"})


@pv.route('/notify', methods=['POST'])
def wx_pay_notify():
    logger.info('进入支付通知处理接口 wx_pay_notify::: ')
    working_app = current_app._get_current_object()
    xml_data = request.get_data()
    decode_xml_data = xml_data.decode('utf-8')
    print(decode_xml_data)

    notify_dic = Utils.xml_to_dict(decode_xml_data)
    return_code = notify_dic['return_code']
    print('notify_dic %s' % notify_dic)
    now_time = int(time.time())
    if return_code == 'SUCCESS':
        result_code = notify_dic['result_code']
        if result_code == 'SUCCESS':
                    be_verify_sign = notify_dic['sign']
                    del notify_dic['sign']
                    logger.info('开始验证签名--------------------')
                    local_sign = Utils.create_sign(Utils,notify_dic, working_app.config['MERCH_KEY'])
                    if not Utils.verify_notify_sign(Utils,local_sign, be_verify_sign):  # 验证微信支付结果通知签名
                        logger.info('支付结果通知签名信息有问题--------------------')
                        return '''
                                <?xml version="1.0" encoding="utf-8"?>
                                          <return_code><![CDATA[ERROR]]></return_code>
                                          <return_msg><![CDATA[OK]]></return_msg>
                                </xml>
                                '''

                    openid = notify_dic['openid']
                    mch_id = notify_dic['mch_id']
                    nonce_str = notify_dic['nonce_str']
                    appid = notify_dic['appid']
                    total_fee = notify_dic['total_fee']
                    out_trade_no = notify_dic['out_trade_no']
                    attach = notify_dic['attach']
                    time_end = notify_dic['time_end']
                    transaction_id = notify_dic['transaction_id']
                    logger.info('wx_pay_notify: 系统开始处理此订单的支付状态::: ' + out_trade_no)
                    try:
                            order_info = Orders.query.filter(Orders.order_no == out_trade_no).first()
                            order_type = order_info.order_type
                            # 订单信息异常
                            if order_info is None:
                                logger.info('wx_pay_notify: 查无此订单::: ' + out_trade_no)
                                return
                                '''
                                         <xml>
                                          <return_code><![CDATA[SUCCESS]]></return_code>
                                          <return_msg><![CDATA[OK]]></return_msg>
                                        </xml>
                                '''
                            if 'payed' == order_info.status or 'complete' == order_info.status:
                                logger.info('wx_pay_notify: 系统已经处理此订单::: ' + out_trade_no)
                                return '''
                                  <xml>
                                      <return_code><![CDATA[SUCCESS]]></return_code>
                                      <return_msg><![CDATA[OK]]></return_msg>
                                    </xml>
                                 '''
                            order_info.status = 'payed'
                            order_info.finish_time = Utils.util_settle_time(Utils,time_end, 0)

                            channel_pay = ChannelPay.query.filter(ChannelPay.out_trade_no == out_trade_no).first()
                            channel_pay.openid = openid
                            channel_pay.mch_id = mch_id
                            channel_pay.attach = attach
                            channel_pay.transaction_id = transaction_id
                            channel_pay.out_trade_no = out_trade_no
                            channel_pay.total_fee = total_fee
                            channel_pay.pay_time = Utils.util_settle_time(Utils,time_end, 0)
                            channel_pay.status = 'success'

                            transaction_type = 'enroll'
                            if order_type in ['member']:
                                transaction_type = 'member'
                                attach = order_info.attach
                                member_type = attach.get('member_type', 'silver')
                                member = create_member(member_type, order_info.merchant_id, order_info.id)
                                db.session.add(member)

                            settle_time = Utils.util_settle_time(Utils,time_end, 2)  # T+1结算 结算日 1+1
                            transaction = Transaction(pay_id=str(channel_pay.id), merchant_id=order_info.merchant_id,
                                                      order_no=out_trade_no, amount=int(total_fee), type=transaction_type,
                                                      status='unsettle', create_time=now_time, settle_time=settle_time)

                            content = {'scene': 'attention', 'order_no': out_trade_no, 'title': order_info.title,
                                       'img_url': order_info.img_url,
                                       'price': order_info.price, 'shares': order_info.shares,
                                       'amount': int(total_fee)}
                            content = json.dumps(content, ensure_ascii=False)
                            notify_message = Message(sender_id=app.config['platform_id'], sender_name='校云宝',
                                                     receiver_id=order_info.merchant_id,
                                                     receiver_name='商户机构', message_type='notify', content=content,
                                                     create_time=now_time)
                            # TODO:
                            if order_type in ['activity', 'course']:
                                tasks.async_add_reward.apply_async(args=[order_info.id],
                                                                   queue='ADD_REWARD_QUEUE')  # 指定消息队列
                            db.session.add(notify_message)
                            db.session.add(transaction)
                            db.session.commit()

                            logger.info('wx_pay_notify: 系统生成一笔交易流水::: ' + 'pay_id: ' + str(channel_pay.id) + '  order_no:'+
                                        out_trade_no + '  amount: '+ total_fee + ' merchant_id: '+str(order_info.merchant_id))
                            return '''
                                         <xml>
                                                  <return_code><![CDATA[SUCCESS]]></return_code>
                                                  <return_msg><![CDATA[OK]]></return_msg>
                                        </xml>
                                    '''

                    except:
                        print_exc()
                        db.session.rollback()
    return '''
         <?xml version="1.0" encoding="utf-8"?>
                  <return_code><![CDATA[ERROR]]></return_code>
                  <return_msg><![CDATA[OK]]></return_msg>
        </xml>
    '''


@pv.route('/reward', methods=['POST'])
def add_reward():
    #from celerys.tasks import async_add_reward
    #async_add_reward.apply_async(args=[161], queue='ADD_REWARD_QUEUE')
    return jsonify({})


@pv.route('/unipay', methods=['POST'])
@identify_required
def unipay():
    """小程序调起支付所需的签名数据
        @@@
        #### args

        | args | nullable | type | remark |
        |--------|--------|--------|--------|
        |    order_no    |    false    |    string   |    订单编号  |


        #### return
        - ##### json
        >  {"code": "success","data": {"appId" :"44444idjuej","mch_id" :"44444idjuej","nonceStr" :"44444idjuej",
        "package" :"prepay_id=wx2017033010242291fcfe0db70013231072","signType":"MD5","timeStamp" :14678909,"paySign":"22D9B4E54AB1950F51E0649E8810ACD6"}
        @@@
    """
    working_app = current_app._get_current_object()
    url_root = request.url_root

    pay_notify_url = url_root + working_app.config['NOTIFY_URL']
    json_data = request.json
    order_no = json_data.get('order_no', None)

    if request.headers.getlist("X-Forwarded-For"):
        spbill_create_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        spbill_create_ip = request.remote_addr

    print('spbill_create_ip %s' % spbill_create_ip)

    order_info = Orders.query.filter(Orders.order_no == order_no).first()
    if not order_info:
        return jsonify({"code": "error", "info": "支付订单数据异常"})
    user_id = order_info.user_id
    product_id = order_info.product_id
    order_amount = order_info.order_amount
    prepay_id = order_info.prepay_id
    nonce_str = Utils.get_nonce_str(Utils)
    merchant_id = order_info.merchant_id
    if prepay_id:
        package = 'prepay_id=' + prepay_id
        now_time = int(time.time())
        pay_dict_data = {"appId": working_app.config['WX_APPID'], "nonceStr": nonce_str, "package": package, "signType": "MD5",
                         "timeStamp": now_time}
        pay_sign = Utils.create_sign(Utils, pay_dict_data, working_app.config['MERCH_KEY'])
        pay_dict_data['paySign'] = pay_sign
        return jsonify({"code": "success", "data": pay_dict_data})
    else:
        openid = g.user.openid
        attach = 'merchant_id=' + str(order_info.merchant_id) + '|'+'user_id=' + str(order_info.user_id) \
                 + '|' + 'product_num=' + str(order_info.shares)
        body = '活动/课程' + "-" + "校云宝"
        dict_data = {"appid": working_app.config['WX_APPID'], "mch_id": working_app.config['MERCH_ID'], "nonce_str": nonce_str,
                     "body": body, "out_trade_no": order_no,
                     "total_fee": int(order_amount), "spbill_create_ip": spbill_create_ip,
                     "notify_url": pay_notify_url,
                     "trade_type": "JSAPI", "attach": attach, "product_id": product_id, "openid": openid}

        sign = Utils.create_sign(Utils,dict_data, working_app.config['MERCH_KEY'])
        dict_data['sign'] = sign
        pre_pay_result = pay_api.unified_order(user_id, merchant_id, dict_data, 60)

        if 'success' == pre_pay_result['code']:
            prepay_id = pre_pay_result['prepay_id']
            try:
                order_api.update_order_paying(order_no, prepay_id)
            except:
                print_exc()
                return jsonify(pre_pay_result)

            package = 'prepay_id=' + prepay_id
            now_time = int(time.time())
            pay_dict_data = {"appId": working_app.config['WX_APPID'], "nonceStr": nonce_str, "package": package,
                             "signType": "MD5", "timeStamp": now_time}
            pay_sign = Utils.create_sign(Utils,pay_dict_data, working_app.config['MERCH_KEY'])
            pay_dict_data['paySign'] = pay_sign
            return jsonify({"code": "success", "data": pay_dict_data})
        else:
            return jsonify(pre_pay_result)


def create_member(member_type, merchant_id,order_id):

    now = datetime.datetime.now()
    if member_type == "diamond":
        delta = relativedelta(years=5)
    elif member_type == "gold":
        delta = relativedelta(years=3)
    else:
        delta = relativedelta(years=1)
    member = Member.query.filter_by(merchant_id=merchant_id).order_by(Member.id.desc()).first()
    if member:
        old_expire_time = datetime.datetime.fromtimestamp(member.expire_time)
        expire_time = max(old_expire_time, now) + delta
    else:
        expire_time = now + delta
    member = Member(merchant_id=merchant_id, type=member_type, status="valid", order_id=order_id,
                    expire_time=int(expire_time.timestamp()),create_time=int(time.time()))
    return member