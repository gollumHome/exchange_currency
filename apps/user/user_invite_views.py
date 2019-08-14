# -*- coding: utf-8 -*-
import re
import time
import logging
import json
from apps.utils import md5
from traceback import print_exc
from apps.utils import Utils
from flask import jsonify, request
from apps.utils import response_wrapper
from apps import db, tc_oss, tc_sms
from apps.user import uv
from apps.models import *
from apps.auths import Auth
from apps.aliyun_oss import AliyunOss
from apps.user.user_controller import UserApi
from apps.email_service import EmailApi
from apps.constant import USER_STATUS
from apps.order.db_submit_controller import AtoSubmit
from apps.constant import REWARD_STATUS
from flask import app
from flask import current_app




from apps.utils import rand_str
aliyun_oss = ''
mail_api = ''

logger = logging.getLogger()


@uv.route('/invite_register/', methods=['POST'])
def user_invite_register():
    """【邀请注册】
       url格式： /api/v1/user/invite_register/?
      @@@
      #### args
        | args | nullable | type | remark |
        |--------|--------|--------|--------|
        | email |    false    |    string   |  注册邮箱 |
        | password |    false    |    string   |  密码 |
        | invite_code |    false    |    string   |  邀请码 |
         #### return
        - ##### json
       >  {"code": "200"}
        @@@
      """
    user_id = 1
    data = json.load(request.data)
    password = data.get('password', '')
    email = data.get('email', '')
    invite_code = data.get('invite_code', '')

    if email == '' or password == '' or invite_code == '':
        return jsonify({"code": "400", "info": "缺少关键参数"})
    try:
        with AtoSubmit(db):
            data['status'] = REWARD_STATUS['bereward']
            user_api.invite_recrod(data)
            data['user_id'] = user_id
            data['status'] = USER_STATUS['normal']
            user_api.register(data)
        return jsonify({"code": "200", 'info': "注册成功，请重新登陆"})
    except Exception:
        logger.error(print_exc())
        return jsonify({"code": "500", 'info': "注册成功，请重新登陆"})


@uv.route('/invite_history/', methods=['GET'])
def user_invite_register_history():
    """【邀请注册 历史查询】
       url格式： /api/v1/user/invite_history/
      @@@
      #### args
        | args | nullable | type | remark |
        |--------|--------|--------|--------|
        | page |    trure    |    string   |   |
        | size |    true    |    string   |   |
         #### return
        - ##### json
       >  {"code": "200"}
        @@@
      """
    user_id = 1
    data = json.load(request.data)
    page = data.get('page', 1)
    size = data.get('size', 10)

    obj_list = user_api.get_invite_recrod_list(user_id, page, size)
    resp_data = list()
    if obj_list:
        for obj in obj_list:
            resp_data.append({
                "share_id": obj.share_id,
                "user_id": user_id,
                "title": obj.title,
                "amount": obj.amount,
                "status": obj.status,
                "create_time": obj.create_time,
                "finish_time": obj.finish_time})
    if not obj_list:
        resp_data = []
    view_data = dict()
    view_data['code'] = '200'
    view_data['data'] = resp_data
    return jsonify(view_data)


