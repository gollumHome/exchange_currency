#!/usr/bin/env python
# coding: utf-8

###############################################################
#   工具类
###############################################################

import time
import uuid
import random
import hashlib
import logging
import traceback
from functools import wraps
import xml.etree.ElementTree as elementTree

from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from apps import db

logger = logging.getLogger(__name__)


def parse_offset_limit(request):
    offset = int(request.args.get("offset") or 0)
    limit = int(request.args.get("limit") or 20)

    if offset < 0:
        offset = 0
    if limit < 5 or limit > 100:
        limit = 20
    if "page" in request.args or "size" in request.args:
        page = int(request.args.get('page') or 1)
        size = int(request.args.get('size') or 20)
        if page < 1:
            page = 1
        if size < 5 or size > 100:
            size = 20
        offset = (page - 1) * size
        limit = size
    return offset, limit


def response_wrapper(func):
    @wraps(func)
    def _inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logger.error(traceback.format_exc())
            db.session.rollback()
            return jsonify({"code": "500", "info": "unknown error", "data": {}})
    return _inner


class Utils(object):
    # 短信验证码
    @staticmethod
    def get_code():
        return str(random.randrange(1000, 9999))

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    @staticmethod
    def check_password(hash, password):
        return check_password_hash(hash, password)

    # 发送短信验证码
    def sendMsm(self, sms, telephone):
        pass

    # 检查手机号和验证码
    @staticmethod
    def checkMsm(tvc, telephone, verify_code):
        data = dict()
        data['code'] = 'error'
        if not telephone or not verify_code:
            data['info'] = "手机号和验证码不能为空"
        else:
            if tvc:
                now = time.time()
                if tvc.dead_line < int(now):
                    data['info'] = "验证码已失效请重新发送"
                else:
                    data['code'] = "success"
            else:
                data['info'] = "验证码错误"
        return data

    @staticmethod
    def get_system_no():
        return str(uuid.uuid4()).replace('-', '')

    def get_nonce_str(self):
        return str(uuid.uuid4()).replace('-', '')

    def create_sign(self, pay_data, merch_key):
        sign_part_front = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        string_sign_temp = '{0}&key={1}'.format(sign_part_front, merch_key)
        md5 = hashlib.md5()
        md5.update(string_sign_temp.encode("utf8"))
        sign = md5.hexdigest()
        return sign.upper()

    def dict_to_xml(self, dict_data):
        xml = ["<xml>"]
        for k, v in dict_data.items():
            xml.append("<{0}>{1}</{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xml_to_dict(xml_data):
        xml_dict = {}
        root = elementTree.fromstring(xml_data)
        for child in root:
            xml_dict[child.tag] = child.text
        return xml_dict

    def verify_notify_sign(self, local_sign, be_verify_sign):
        print('local_sign <--> be_verify_sign %s %s' % (local_sign, be_verify_sign))
        return be_verify_sign == local_sign

    def util_settle_time(self, time_end, delta_day):
        settle_time_struct = time.strptime(time_end, '%Y%m%d%H%M%S')
        settle_time_second = int(time.mktime(settle_time_struct))
        return settle_time_second + delta_day * 24 * 60 * 60

    def str2int_time(self, str_time):
        time_struct = time.strptime(str_time, '%Y-%m-%d %H:%M:%S')
        time_second = int(time.mktime(time_struct))

        return time_second

    def int2str_time(self, int_time):
        time_struct = time.localtime(int_time)  # 秒数
        time_format = time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
        return time_format

    def str2fmt_time(self, str_time):
        return str_time

    def int2curr(self, int_feng):
        float_yuan = int_feng / 100
        return str(float_yuan) + '元'

    if __name__ == '__main__':
        from apps.utils import Utils
        print(Utils.set_password('000000'))