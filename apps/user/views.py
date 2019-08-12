# -*- coding: utf-8 -*-

import re
import time
import logging
import json
from apps.utils import md5


from apps.utils import response_wrapper
from apps import db, tc_oss, tc_sms
from apps.user import uv
from apps.aliyun_oss import AliyunOss
from apps.user.user_controller import UserApi




#aliyun_oss = AliyunOss()
user_api = UserApi(db)

logger = logging.getLogger()


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
          url格式： /api/v1/user/sendcode?telephone=13333333333?verify_type=mch_register
         @@@
         #### args

         | args | nullable | type | remark |
         |--------|--------|--------|--------|
         |    telephone    |    false    |    string   |    手机号  |
         |    verify_type  |    false    |    string   |    验证类型 ['mch_register','add_phone','reset_pass','withdraw'] |

         #### return
         - ##### json
         >  {"code": "200"}
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
        return jsonify({"code": "400", "info": "手机号不能为空"})
    elif not ret:
        return jsonify({"code": "500", "info": "请输入正确的手机号"})
    else:
        # 判断是否已有验证码 （2=有效）
        tvc = TelVerifyCode.query.filter(TelVerifyCode.telephone == telephone,
                                         TelVerifyCode.usable == 2,
                                         TelVerifyCode.verify_type==verify_type).first()
        if tvc:
            if tvc.dead_line > now_time:
                return jsonify({"code": "500", "info": "请务重复发送"})
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
                    return jsonify({'code': '200', "info": "发送成功"})
                else:
                    return jsonify({"code": "500", "info": "请重新发送验证码"})
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
                return jsonify({'code': '200', "info": "发送成功"})
            else:
                return jsonify({"code": "500", "info": "请重新发送验证码"})


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
    > {"code": "200", "imgName": "https://xiaoyunbao-1253692831.cos.ap-shanghai.myqcloud.com/20180912124603_74089.jpg"}
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
            return jsonify({'code': '200', 'img_url': img_url})
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
    json_data = request.json or {}
    email = json_data.get('email', '')
    password = json_data.get('password', '')
    user = User.query.filter(User.email == email).first()
    if user:
        login_status = user_api.loginIn(password, user.salt)
        if login_status:
            return Auth.authenticate(Auth, user, current_app.config['USER_TOKEN_USEFUL_DATE'],
                                     current_app.config['SECRET_KEY'])
        return jsonify({'code': '400', "infog": "账号名或密码错误"})
    return jsonify({'code': '500', "infog": "系统内部错误"})


@uv.route('/user/login_out', methods=['POST'])
def user_login_out():
    """用户登出
    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    user_id    |    false    |    string   |    临时登录凭证    |

    #### return
    - ##### json
    > {"code": "200", "user_id": 202000,"u_token":"4d43082ecddb11e8aa4200163e0f3b60"}
    @@@
    """
    json_data = request.headers.get('user_id')
    user_id = json_data.get('user_id', '')
    if not user_id:
        jsonify({'code': '400', 'info': "参数错误"})
    status = user_api.logout(user_id)
    if status:
        return jsonify({'code': '200', 'info': ''})
    return jsonify({'code': '500', 'info': '内部错误'})


@uv.route('/userinfo', methods=['POST'])
def user_info():
    """修改用户信息
    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    user_name    |    trure    |    string   |    用户昵称   |
    |    head_url    |    trure    |    string   |    用户头像    |
    |    password    |    trure    |    string   |    用户头像    |

    #### return
    - #####
    > {"code":"200"}
    @@@
    """
    user_id = 1
    request_data = request.json
    user_name = request_data.get('user_name', '')
    head_url = request_data.get('head_url', '')
    telephone = request_data.get('telephone','')
    additional_emails = request_data.get('additional_emails', '')
    if user_name == '' and head_url == '' \
            or telephone == '' or additional_emails == '':
        return jsonify({"code": "400", "infog": "请输入正确参数"})

    user = User.query.filter(User.id == int(user_id)).first()
    try:
        if user:
            if user_name:
                user.user_name = user_name
            if head_url:
                user.head_url = head_url
            if telephone:
                user.telephone = telephone
            if additional_emails:
                user.additional_emails = additional_emails
            db.session.commit()
        return jsonify({"code": "200", "info": "更新信息成功"})
    except Exception:
        logger.error(print_exc())
        return jsonify({"code": "500", "info": "更新信息失败"})


@uv.route('/userinfo', methods=['POST'])
def user_reset_password():
    """修改用户信息
    @@@
    #### args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    email    |    false    |    string   |    用户账号  |
    |    confirm    |    true    |    string   |    请求合法校验  |
    |    password    |    true    |    string   |    用户新密码  |

    #### return
    - #####
    > {"code":"200"}
    @@@
    """
    request_data = request.json
    email = request_data.get('email', '')
    confirm = request_data.get('confirm', False)
    password = request_data.get('password', False)
    if email == "":
        return jsonify({"code": "400", "infog": "请输入正确参数"})
    user = User.query.filter(User.email == email).first()
    if not user:
        return jsonify({"code": "400", "infog": "该用户不存在"})
    if confirm:
        reset_status = user_api.update_user_password(user, password)
        if reset_status:
            return jsonify({"code": "200", "infog": "密码重置成功，重新登陆"})
        if not reset_status:
            return jsonify({"code": "500", "infog": "密码重置失败"})
    return jsonify({"code": "403", "infog": "非法请求"})


@uv.route('/register/', methods=['POST'])
def user_register():

    """【注册用户】
       url格式： /api/v1/user/register/?
      @@@
      #### args
        | args | nullable | type | remark |
        |--------|--------|--------|--------|
        | username    |    false    |    string   |   用户名称   |
        | head_url  |    true    |    string   | 用户头像  |
        | telephone     |    false    |    string   |    注册电话  |
        | email |    false    |    string   |  注册邮箱 |
        | ID_verify       |    true    |    string   |   身份证 |
        |  status        |    false    |    string   |   用户状态['normal', 'black', 'beVerified', 'rejected'] |
        |  Passport_verify        |    true    |    string   |   护照|
        |  verify_channel        |    false    |    string   |   认证类型 |
        |  invite_code        |    true    |    string   |   邀请码|
        |  additional_emails        |    true    |    string   |  补充邮箱 |
         #### return
        - ##### json
       >  {"code": "200"}
        @@@
      """
    data = request.json

    user_name = data.get('user_name', '')
    password = data.get('password', '')
    telephone = data.get('telephone', '')
    email = data.get('email', '')
    verify_channel = data.get('verify_channel', '')

    if user_name == '' or telephone == ''\
        or email == '' or verify_channel == '' \
            or password == '':
        return jsonify({"code": "400", "info": "缺少关键参数"})

    success = user_api.register(data)
    if not success:
        return jsonify({"code": "500", 'info': "注册失败"})
    return jsonify({"code": "200", 'info': "注册成功，请重新登陆"})






