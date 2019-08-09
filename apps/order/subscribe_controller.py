# coding: utf-8


import logging
from threading import Thread
from apps.models import *

from apps.redis_client import RedisClient
from apps.order.constant import PROCESS_STATUS_EXPIRE_TIME

from traceback import print_exc

LOG =logging.getLogger(__name__)


class SubscribeApi(object):
    def __init__(self, db):
        self.db = db
        self.sub_client = RedisClient()

    def subscribe_process_exchange(self, pk, book_no=None, status=None):
        result = self.sub_client.subscribe_set_keyvalues(pk, book_no)
        if not result:
            return False
        if status == 'matched':
            expire_time = PROCESS_STATUS_EXPIRE_TIME['matched']
            expired_result = self.sub_client.set_scribe_expired(pk, expire_time)
            if not expired_result:
                return False
        if status == 'set_wallet':
            expire_time = PROCESS_STATUS_EXPIRE_TIME['set_wallet']
            expired_result = self.sub_client.set_scribe_expired(pk, expire_time)
            if not expired_result:
                return False
        if status == 'pending':
            expire_time = PROCESS_STATUS_EXPIRE_TIME['pending']
            expired_result = self.sub_client.set_scribe_expired(pk, expire_time)
            if not expired_result:
                return False
        if status == 'sended':
            expire_time = PROCESS_STATUS_EXPIRE_TIME['sended']
            expired_result = self.sub_client.set_scribe_expired(pk, expire_time)
            if not expired_result:
                return False
        return True

