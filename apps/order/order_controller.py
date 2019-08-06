#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################
#   订单服务类
###############################################################

from traceback import print_exc
import time
import logging
from sqlalchemy import *
from apps.utils import Utils

from apps.order.models import MakerOrder
from apps.models import  User

LOG =logging.getLogger(__name__)


class OrderApi(object):
    def __init__(self, db):
        self.db = db  # 数据库实例子

    def init_from_db(self, db):
        self.db = db

    @staticmethod
    def currency_exchange(hold_currency, hold_amount,
                          exchange_currency,
                          exchange_rate):
        if hold_currency == '' and exchange_currency == '':
            exchange_amount = hold_amount * exchange_rate
            return exchange_amount
        return 0

    @staticmethod
    def get_current_exchange_rate():
        return 0.08

    def get_order_by_pk(self, pk):
        try:
            order_obj = self.db.session.query(MakerOrder).\
                filter(MakerOrder.id == pk).first()
            return order_obj
        except:
            LOG.error(print_exc())
        return None

    def create_maker_order(self, user_id, book_no, hold_currency,
                           hold_amount, exchange_currency,
                           exchange_amount, exchange_rate, status):

        try:
            now_time = int(time.time())
            maker_order_obj = MakerOrder(book_no=book_no,
                                         user_id=user_id,
                                         hold_currency=hold_currency,
                                         exchange_currency=exchange_currency,
                                         hold_amount=hold_amount,
                                         exchange_amount=exchange_amount,
                                         exchange_rate=exchange_rate,
                                         create_time=now_time,
                                         status=status)
            self.db.session.add(maker_order_obj)
            self.db.session.flush()
            self.db.session.commit()
            return {"code": "200", "book_no": book_no}
        except Exception, e:
            self.db.session.rollback()
            LOG.error("create maker order err%s" % print_exc())
        return {"code": "500", "info": "订单生产异常"}

    def create_taker_order(self, user_id, book_no, hold_currency,
                           hold_amount, exchange_currency,
                           exchange_amount, exchange_rate, status):
        try:
            now_time = int(time.time())
            maker_order_obj = MakerOrder(book_no=book_no,
                                         user_id=user_id,
                                         hold_currency=hold_currency,
                                         exchange_currency=exchange_currency,
                                         hold_amount=hold_amount,
                                         exchange_amount=exchange_amount,
                                         exchange_rate=exchange_rate,
                                         create_time=now_time,
                                         status=status)
            self.db.session.add(maker_order_obj)
            self.db.session.flush()
            self.db.session.commit()
            return {"code": "200", "book_no": book_no}
        except Exception, e:
            self.db.session.rollback()
            LOG.error("create maker order err%s" % print_exc())
        return {"code": "500", "info": "订单生产异常"}

