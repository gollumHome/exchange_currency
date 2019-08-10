# coding: utf-8

import os
import time
import logging
from apps.order import ov
from flask import jsonify, request
from flask import current_app
from apps.order.sms_controller import SmsController


from apps.models import *

sms_api = SmsController()
aliyun_oss = ''
logger = logging.getLogger(__name__)


ALLOWED_EXTENSIONS = ['png', 'jpg', 'JPG', 'PNG', 'bmp']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@ov.route('/taker_order/upload_proof/', methods=['POST'])
def upload_taker_order_proof():
    pk = request.args.get('pk')
    obj = TakerOrder.query.filter(id=pk)
    if not obj:
        return jsonify({'code': 500, 'info': '读取吃单对象异常'})

    if request.method == 'POST':
        file = request.files['file']
        if not (file and allowed_file(file.filename)):
            return jsonify({"code": 400, "info": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        try:
            file_name = str(obj.user_id)+str(obj.book_no)+str(time.time())
            aliyun_oss.upload_image('no',file_name,file)
        except Exception as e:
            logger.error(e)
            return jsonify({"code": 500, "info": "上传图片失败"})


@ov.route('/maker_order/upload_proof/', methods=['POST'])
def upload_maker_order_proof():
    pk = request.args.get('pk')
    obj = MakerOrder.query.filter(id=pk)
    if not obj:
        return jsonify({'code': 500, 'info': '读取吃单对象异常'})

    if request.method == 'POST':
        file = request.files['file']
        if not (file and allowed_file(file.filename)):
            return jsonify({"code": 400, "info": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        try:
            file_name = str(obj.user_id)+str(obj.book_no)+str(time.time())
            aliyun_oss.upload_image('no', file_name, file)
        except Exception as e:
            logger.error(e)
            return jsonify({"code": 500, "info": "上传图片失败"})