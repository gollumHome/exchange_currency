# -*- coding: utf-8 -*-

import os
import datetime
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))
database_uri = os.environ.get('TEST_DATABASE_URL')


class Config:
    API_DOC_MEMBER = ["activity", "course", "order", "pay", "merchant", "api", "platform"]  # 需要显示文档的 Api
    RESTFUL_API_DOC_EXCLUDE = []  # 需要排除的 RESTful Api 文档
    JSON_AS_ASCII = False
    # secret_key setting
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    # database setting
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_ECHO = False


    # oss key setting
    OSS_ACCESSKEY_ID = 'LTAIpNbyB8MrXdVY'
    OSS_ACCESSKEY_SECRET = '6ugz9ApEFStCbkL1jDyG6PRCEEaO1U'
    OSS_PUBLIC_BUCKET = 'jk-pub'
    OSS_PRIVATE_BUCKET = 'jk-auth'

    # tencent sms setting
    SMS_APP_ID = '1400207708'
    SMS_APP_KEY = '873d9b3909ba3ac38eb2df3e985bd7d3'
    # 区域,可选
    TENCENT_API_REGION_ID = "cn-hangzhou"

    TENCENT_SMS_GATEWAY = "https://dysmsapi.aliyuncs.com/"
    TELEPHONE_TEMPLATE_ID = "330333"  # 完善手机号码模版
    RESET_TEMPLATE_ID = "330327"  # 重置密码
    WITHDRAW_TEMPLATE_ID = "330324"  # 商户申请提现
    MERCHANT_TEMPLATE_ID = "330318"  # 商户注册
    # 验证码有效期 （5分钟）
    VERIFY_USEFUL_DATE = '300'

    # pagination
    PER_PAGE = '10'
    # Token
    ADMIN_TOKEN_USEFUL_DATE = datetime.timedelta(days=7)
    USER_TOKEN_USEFUL_DATE = datetime.timedelta(hours=24)

    # wx pay setting
    WX_SESSION_URL = 'https://api.weixin.qq.com/sns/jscode2session'
    WX_APPID = 'wx5f0f77612aac273a'
    WX_APP_SECRET = '120a8288959507549ca13d6ace0ab37c'
    MERCH_ID = '1486942472'
    MERCH_KEY = 'j4aowpstckyj3ua4wp5cjcj2bqykdmtg'
    NOTIFY_URL = 'api/notify'
    REFUND_NOTIFY_URL = ''
    SPBILL_CREATE_IP = '118.25.15.146'

    PLATFORM_ID = '1000000001'  # 平台id
    WX_ACCESSTOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'
    MINI_TEMPLATE_URL = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send'

    # fee setting
    WITHDRAW_FEE_RATE = '1.60'


    access_token = ""

    ADMIN_USER = ''
    ADMIN_PASSWORD = ''

    DEFAULT_DIAGRAM = 'https://xiaoyunbao-1253692831.cos.ap-shanghai.myqcloud.com/adaef4c55e07480687b48c805d5faf4f.png'
    MP_WXCODE_URL = 'https://xiaoyunbao-1253692831.cos.ap-shanghai.myqcloud.com/adaef4c55e07480687b48c805d5faf4f.png'

    MAIL_SENDER = ''
    MAIL_PASSWORD = ''
    SMTP_SERVER = ''
    SMTP_PORT = 25

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:nas@mhm1234@139.196.78.95:3306/JK-exchange?charset=utf8mb4'
    REDIS_SERVER_HOST = '127.0.0.1'


# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:nas@mhm1234@139.196.78.95:3306/JK-exchange-test?charset=utf8mb4'
#     ELASTIC_SEARCH_HOST = ''
#     CERT_PATH = '/usr/local/www/cert'
#     CDN_STATIC_PATH = tempfile.gettempdir()
#     CDN_STATIC_URL = 'http://cdn.liyun.com/static/'
#     REDIS_SERVER_HOST = '127.0.0.1'
#
#
# class Testing2Config(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:nas@mhm1234@139.196.78.95:3306/JK-exchange-test?charset=utf8mb4'
#     ELASTIC_SEARCH_HOST = ''
#     CERT_PATH = '/usr/local/www/cert'
#     CDN_STATIC_PATH = tempfile.gettempdir()
#     CDN_STATIC_URL = 'http://cdn.liyun.com/static/'
#     REDIS_SERVER_HOST = '127.0.0.1'


# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:nas@mhm1234@139.196.78.95:3306/JK-exchange?charset=utf8mb4'
#     CERT_PATH = '/usr/local/www/cert'
#     SERVICE_CATE_ID = ''
#     CDN_STATIC_PATH = '/usr/local/xiaoyunbao/static/'
#     CDN_STATIC_URL = 'http://static.xiaoyunbao.com.cn/'
#     REDIS_SERVER_HOST = '127.0.0.1'


config = {
    #'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'testing2': Testing2Config,
    # 'production': ProductionConfig,
    'default': DevelopmentConfig
}
