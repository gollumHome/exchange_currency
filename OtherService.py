#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################
#   系统其它服务类
###############################################################

import requests
import json

import uuid

from traceback import print_exc
from flask import jsonify
from apps import db, tc_oss

from apps.utils import Utils


class OtherApi(object):
    def __init__(self):
        self.GET_WXACODE_URL = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token='   # 取得小程序码

    def get_wxacode(self, dict_params, access_token):

        json_params = json.dumps(dict_params)
        print(json_params)
        try:
            url = self.GET_WXACODE_URL + access_token
            res = requests.post(url=url, headers={'Content-Type': 'text/json'}, data=json_params)

            if isinstance(res.content, str):
                print("error")
            else:
                img_name = str(uuid.uuid4())
                img_url = tc_oss.upload_image(img_name, res.content)
                return {'code': 'success', 'img_url': img_url}
        except:
            print_exc(limit=5)
        return {"code": "error"}

