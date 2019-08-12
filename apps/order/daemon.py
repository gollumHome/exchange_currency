# coding: utf-8

import flask
import time
import logging
from config import config
from apps.models import *
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['default'].SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)


from apps.redis_client import RedisClient


logger = logging.getLogger(__name__)


class Monitor_order_expired:
    def __init__(self):
        self.sub_client = RedisClient()
        self.sub_obj = self.sub_client.get_scribe_obj()
        self.sub_scribe_event()

    def start_monitro(self):
        while True:
            message = self.sub_obj.get_message()
            if message:
                print(message)
            else:
                time.sleep(0.01)

    def sub_scribe_event(self):
        param = dict()
        param['__keyevent@0__:expired'] = self.hand_subscribe_message
        print(self.sub_obj.psubscribe(**param))

    def hand_subscribe_message(self, message):
        data = message
        pk = data['data']
        try:
            exproces_obj = db.session.query(ExchangeProgres). \
                filter(ExchangeProgres.id == pk).first()
            if exproces_obj:
                exproces_obj.status = 'canceled'
                logger.info('order no %s is expired',exproces_obj.book_no)
            db.session.flush()
            db.session.commit()
        except Exception as e:
            logger.error('set order no %s  expired err', e)


monitor = Monitor_order_expired()
monitor.start_monitro()