# -*- coding: utf-8 -*-

import re
import time
import logging
import json

import urllib.parse
import urllib.request


from apps.utils import response_wrapper
from apps import db, tc_oss, tc_sms
from apps.user import uv


from apps.common import *

logger = logging.getLogger()


@uv.route("/")
def hello():
    return jsonify({"message": "Hello, user!"})


@uv.route("/sendsms", methods=['GET'])
def sms_valid():
    phone_number = request.args.get('phone_number', None)
    params = ['2089', '2']
    result = tc_sms.send_sms(phone_number, params, 'add_phone')
    print(result)
    return jsonify(result)


@uv.route('/sendcode', methods=['GET'])
def send_code():
    """【发送验证码】
          url格式： /api/sendcode?telephone=13333333333?verify_type=mch_register
         @@@
         #### args

         | args | nullable | type | remark |
         |--------|--------|--------|--------|
         |    telephone    |    false    |    string   |    手机号  |
         |    verify_type  |    false    |    string   |    验证类型 ['mch_register','add_phone','reset_pass','withdraw'] |

         #### return
         - ##### json
         >  {"code": "success"}
         @@@
         """
    telephone = request.args.get('telephone', None)
    verify_type = request.args.get('verify_type', None)
    logger.warning(type(telephone))
    now_time = int(time.time())
    telephone = telephone
    ret = re.match(r"^1[356789]\d{9}$", telephone)
    working_app = current_app._get_current_object()
    if telephone is None:
        return jsonify({"code": "error", "info": "手机号不能为空"})
    elif not ret:
        return jsonify({"code": "error", "info": "请输入正确的手机号"})
    else:
        # 判断是否已有验证码 （2=有效）
        tvc = TelVerifyCode.query.filter(TelVerifyCode.telephone == telephone, TelVerifyCode.usable == 2, TelVerifyCode.verify_type==verify_type).first()
        if tvc:
            if tvc.dead_line > now_time:
                return jsonify({"code": "error", "info": "请务重复发送"})
            else:
                tvc.usable = 1
                db.session.commit()
                verifyCode = Utils.get_code()
                params = [str(verifyCode), working_app.config['VERIFY_USEFUL_DATE']]
                smsInfo = tc_sms.send_sms(telephone, params, verify_type)

                if smsInfo['result'] == 0:
                    create_time = int(time.time())
                    dead_line = create_time + int(working_app.config['VERIFY_USEFUL_DATE'])

                    # 插入手机验证码表
                    telVerifyInfo = TelVerifyCode(telephone=telephone, verifyCode=verifyCode,
                                                  create_time=create_time,
                                                  dead_line=dead_line, usable=2,verify_type=verify_type)
                    db.session.add(telVerifyInfo)
                    db.session.commit()
                    return jsonify({'code': 'success', "info": "发送成功"})
                else:
                    return jsonify({"code": "error", "info": "请重新发送验证码"})
        else:
            verifyCode = Utils.get_code()
            params = [str(verifyCode), working_app.config['VERIFY_USEFUL_DATE']]
            smsInfo = tc_sms.send_sms(telephone, params, verify_type)
            if smsInfo['result'] == 0:
                create_time = int(time.time())
                dead_line = create_time + int(working_app.config['VERIFY_USEFUL_DATE'])

                # 插入手机验证码表
                telVerifyInfo = TelVerifyCode(telephone=telephone, verifyCode=verifyCode, create_time=create_time,
                                              dead_line=dead_line, usable=2,verify_type=verify_type)
                db.session.add(telVerifyInfo)
                db.session.commit()
                return jsonify({'code': 'success', "info": "发送成功"})
            else:
                return jsonify({"code": "error", "info": "请重新发送验证码"})


@uv.route("/upload", methods=['POST'])
def upload_img():
    """上传图片
    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    file    |    false    |    bytes   |    文件    |

    #### return
    - ##### json
    > {"code": "success", "imgName": "https://xiaoyunbao-1253692831.cos.ap-shanghai.myqcloud.com/20180912124603_74089.jpg"}
    @@@
    """
    try:
        img_name = Utils.get_system_no()
        file = request.files['file']
        file_extention = file.filename.rsplit('.', 1)[1]
        print(file_extention)
        if file:
            file_bytes = file.read()
            img_name = img_name + "." + file_extention
            img_url = tc_oss.upload_image(img_name,file_bytes)
            return jsonify({'code': 'success', 'img_url': img_url})
    except:
        print_exc(limit=5)
    return jsonify({'code': 'error'})


@uv.route('/user/login', methods=['POST'])
def user_login():
    """用户登陆
    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    code    |    false    |    string   |    临时登录凭证    |

    #### return
    - ##### json
    > {"code": "success", "user_id": 202000,"u_token":"4d43082ecddb11e8aa4200163e0f3b60"}
    @@@
    """
    try:
            json_data = request.json or {}
            jscode = json_data.get("code", None)
            print(jscode)
            wx_session_url = current_app.config['WX_SESSION_URL']
            params = urllib.parse.urlencode({'appid':current_app.config['WX_APPID'],'secret':current_app.config['WX_APP_SECRET'],'js_code':jscode,'grant_type':'authorization_code'})
            params = params.encode('utf-8')
            with urllib.request.urlopen(wx_session_url, params, timeout=2) as f:
                    openid_data = f.read().decode('utf-8')
                    openid_data = json.loads(openid_data)
                    print('openid_data %s' % openid_data)
                    if 'openid' in openid_data:
                            openid = openid_data['openid']
                            session_key = openid_data['session_key']
                            user = User.query.filter_by(openid=openid).first()
                            if user:
                                user.session_key = session_key
                            else:
                                now_time = int(time.time())
                                try:
                                    user = User(openid=openid, session_key=session_key, create_time=now_time,
                                                status='normal')
                                    db.session.add(user)
                                    db.session.commit()
                                except:
                                    print_exc()

                            return Auth.authenticate(Auth, user, current_app.config['USER_TOKEN_USEFUL_DATE'],
                                                     current_app.config['SECRET_KEY'])

    except urllib.error.URLError as e:
        logging.ERROR(e)
    except:
        print_exc()
    return jsonify({'code': 'error'})


@uv.route('/userinfo', methods=['POST'])
@response_wrapper
@identify_required
def user_info():
    """保存用户信息
    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    nickname    |    false    |    string   |    用户昵称   |
    |    avatar_url    |    false    |    string   |    用户头像    |

    #### return
    - #####
    > {"code":"success"}
    @@@
    """
    user_id = g.user_id
    request_data = request.get_data(as_text=True)
    json_data = json.loads(request_data)
    nickname = json_data['nickname']
    avatar_url = json_data['avatar_url']

    user = User.query.filter(User.id == int(user_id)).first()
    if user:
         user.nickname = nickname
         user.head_url = avatar_url
         db.session.commit()
         return jsonify({"code": "success"})
    else:
         return jsonify({"code": "error"})



