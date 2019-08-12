# -*- coding: utf-8 -*-

import flask
from flask_sqlalchemy import SQLAlchemy

from config import config
from .tencent_sms import TencentSms
from .tencent_oss import TencentOss
from .redis_client import RedisClient

db = SQLAlchemy()
tc_sms = TencentSms()
tc_oss = TencentOss()
redis_client = RedisClient()


def create_app(config_name):
    from apps.order import ov
    # from apps.pay import pv
    # from apps.user import uv
    # from apps.backend import bv
    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    #app.register_blueprint(uv)

    app.register_blueprint(ov)
    # app.register_blueprint(pv)
    # app.register_blueprint(bv)
    #
    # tc_sms.init_from_app(app)
    # tc_oss.init_from_app(app)
    # redis_client.init_from_app(app)

    return app
