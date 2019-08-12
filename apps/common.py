# -*- coding: utf-8 -*-

import json
import logging
import time
from functools import wraps
from traceback import print_exc

from flask import request, current_app, jsonify, g
from sqlalchemy import and_
from threading import Thread

from apps.auths import Auth
from apps.models import User, TelVerifyCode,  AdminUser
from apps.utils import Utils
from OtherService import OtherApi

logger = logging.getLogger(__name__)

other_api = OtherApi()


def asyncX(func):
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def access_token_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        working_app = current_app._get_current_object()
        data = Auth.identify(Auth, auth_header, working_app.config['SECRET_KEY'])
        if (not data) or data['code'] == "error":
            return jsonify(data)
        return func(*args, **kwargs)
    return decorated_function


def identify_required(func):
    func.__doc__ = (func.__doc__ or "").replace("@@@", "@@@\n### permission\nUser(用户权限)", 1)
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        print('auth_header ', auth_header)
        working_app = current_app._get_current_object()
        data = Auth.identify(Auth, auth_header, working_app.config['SECRET_KEY'])
        logger.info(data)
        try:
            if 'user_id' in data:
                g.user_id = data['user_id']
                g.user: User = data["data"]
            else:
                return jsonify(data)
        except:
            print_exc(limit=3)
        return func(*args, **kwargs)
    return decorated_function


def optional_identify_required(func):
    func.__doc__ = (func.__doc__ or "").replace("@@@", "@@@\n### permission\nOptional User(可选的用户权限)", 1)

    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        working_app = current_app._get_current_object()
        data = Auth.identify(Auth, auth_header, working_app.config['SECRET_KEY'])
        logger.info(data)
        try:
            if 'user_id' in data:
                g.user: User = data["data"]
            else:
                g.user = None
        except:
            print_exc(limit=3)
        return func(*args, **kwargs)
    return decorated_function


def admin_identify_required(func):
    func.__doc__ = (func.__doc__ or "").replace("@@@", "@@@\n### permission\nAdmin(管理员权限)", 1)

    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        working_app = current_app._get_current_object()
        data = Auth.admin_identify(auth_header, working_app.config['SECRET_KEY'])
        if (not data) or data['code'] == "error":
            return jsonify(data)
        g.admin: AdminUser = data["data"]
        return func(*args, **kwargs)
    return decorated_function


# 短信码拦截验证机制
def verify_code_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        json_data = request.json or {}
        telephone = json_data['telephone']
        print('telephone1',telephone)
        verify_code = json_data['verify_code']
        verify_type = json_data['verify_type']
        logger.info(verify_code)
        try:
            tvc: TelVerifyCode = TelVerifyCode.query.filter(and_(TelVerifyCode.telephone == telephone,
                                                                 TelVerifyCode.verify_type == verify_type)).first()
            if not tvc:
                return jsonify({"code": "error", "info": "no such telephone"})
            ret = Utils.checkMsm(tvc, telephone, verify_code)
            if ret["code"] == "error":
                return ret
        except:
            print_exc(limit=3)
        return func(*args, **kwargs)
    return decorated_function


