# coding: utf-8

import logging
from apps.models import *
from apps.redis_client import RedisClient


LOG =logging.getLogger(__name__)


class SubscribeApi(object):
    def __init__(self, db):
        self.db = db
        self.sub_client = RedisClient()
        self.sub_obj = self.sub_client.get_scribe_obj()
        self.sub_scribe_event()

    def sub_scribe_event(self):
        param = dict()
        param['__keyevent@0__:expired'] = self.hand_subscribe_message
        self.sub_obj.psubscribe(**param)

    def hand_subscribe_message(self, message):
        data = message
        pk = data['data']
        exproces_obj = self.db.session.query(ExchangeProgres). \
            filter(ExchangeProgres.id == pk).first()
        if exproces_obj:
            exproces_obj.status = 'cancled'
            LOG.info('order no %s is expired',exproces_obj.book_no)

    def subscribe_process_exchange(self, pk, book_no=None, status=None):
        self.sub_client.subscribe_set_keyvalues(book_no, book_no)
        if status == '':
            expire_time = 5
            self.sub_client.set_scribe_expired(book_no, expire_time)
        if status == '':
            expire_time = 5
            self.sub_client.set_scribe_expired(book_no, expire_time)
        while True:
            # todo when order status update from one to another , remove subsribe and break loop
            exproces_obj = self.db.session.query(ExchangeProgres). \
                filter(ExchangeProgres.id == pk).first()
            if exproces_obj:
                if exproces_obj.status != status:
                    break
