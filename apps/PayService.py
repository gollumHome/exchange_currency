#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################
#   支付服务类
###############################################################

import requests
import time
import ssl

from traceback import print_exc


from apps.utils import Utils


UNIFIED_ORDER_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder'   # 微信支付统一下单地址
PAY_REFUND_URL = 'https://api.mch.weixin.qq.com/secapi/pay/refund'   # 微信支付退款接口
PAY_TRANSFERS_URL = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers'   # 企业付款到零钱


class PayApi(object):
    def __init__(self,db):
        self.db = db  # 数据库实例子

    def init_from_db(self, db):
        self.db = db

    # def get_order_by_no(self, order_no):
    #     try:
    #         order_obj = Orders.query.filter(Orders.order_no == order_no).first()
    #         print('order %s' % order_obj.order_no)
    #         return order_obj
    #     except:
    #         print_exc()
    #     return None

    # def unified_order(self, user_id, merchant_id, dict_data, timeout):
    #     xml_data = Utils.dict_to_xml(Utils,dict_data)
    #     print('xml_data %s' %(xml_data))
    #     try:
    #         r = requests.post(url=UNIFIED_ORDER_URL, headers={'Content-Type': 'text/xml'}, data=xml_data.encode('utf-8'),verify=False)
    #         r.encoding = 'utf-8'
    #         r_dict = Utils.xml_to_dict(r.text)
    #         print(r_dict)
    #         return_code = r_dict['return_code']
    #
    #         if return_code == 'SUCCESS':
    #             result_code = r_dict['return_code']
    #             if result_code == 'SUCCESS':
    #                 prepay_id = r_dict['prepay_id']
    #                 try:
    #                     channel_pay = ChannelPay(out_trade_no=dict_data['out_trade_no'], user_id=user_id,
    #                                              merchant_id=merchant_id, status='paying', create_time=int(time.time()))
    #                     self.db.session.add(channel_pay)
    #                     self.db.session.commit()
    #                 except:
    #                     print_exc()
    #                     return {"code": "error", "err_code_des": "本地服务器异常"}
    #                 return {"code": "success", "prepay_id": prepay_id}
    #             else:
    #                 info = r_dict['err_code_des']
    #                 return {"code": "error", "err_code_des": info}
    #
    #     except:
    #         print_exc()
    #         return {"code": "fail"}

    def pay_transfer(self, cert_path, dict_data, timeout):
        xml_data = Utils.dict_to_xml(Utils,dict_data)
        # print('xml_data %s' % xml_data)
        try:
            r = requests.post(url=PAY_TRANSFERS_URL, headers={'Content-Type': 'text/xml'},
                              data=xml_data.encode('utf-8'), cert=(cert_path+'/apiclient_cert.pem', cert_path+'/apiclient_key.pem'))
            r.encoding = 'utf-8'
            r_dict = Utils.xml_to_dict(r.text)
            print(r_dict)
            return_code = r_dict['return_code']
            if return_code == 'SUCCESS':
                result_code = r_dict['result_code']
                if result_code == 'SUCCESS':
                    return {"code": "success"}
                else:
                    info = r_dict['err_code_des']
                    return {"code": "error", "err_code_des": info}

        except:
            print_exc()
            return {"code": "fail"}


