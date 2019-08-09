# coding: utf-8

import os
import time
from apps.order import ov
from flask import jsonify, request
from werkzeug.utils import secure_filename

from apps.order.sms_controller import SmsController


from apps.models import *

sms_api = SmsController()


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@ov.route('/taker_order/upload_proof/', methods=['POST'])
def upload_taker_order_proof():
    pk = request.args.get('pk')
    obj = TakerOrder.query.filter(id=pk)
    if not obj:
        return jsonify({'code': 500, 'info': '读取吃单对象异常'})

    if request.method == 'POST':
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        try:
            os.rename(f.filename, str(obj.user_id)+str(obj.book_no)+str(time.time()))
            basepath = os.path.dirname(__file__)
            upload_path = os.path.join(basepath, '/images', secure_filename(f.filename))
            f.save(upload_path)
            sms_api.send_2_disputed_info()
        except Exception:
            pass

    view_data = dict()
    if True:
        view_data['code'] = '200'
        view_data['data'] = {}
    else:
        view_data['code'] = '500'
        view_data['info'] = '上传失败'
    return jsonify(view_data)



@ov.route('/maker_order/upload_proof/', methods=['POST'])
def upload_maker_order_proof():
    pk = request.args.get('pk')
    param_data = request.json
    status = param_data.get('status', "")