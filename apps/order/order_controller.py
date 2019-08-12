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

from .constant import TAKER_ORDER_STATUS

from apps.models import MakerOrder,TakerOrder
from apps.order.constant import  ECCHANGE_CURRENCY_TYPE
from apps.order.exchange_process_controller import ProcesApi
from apps.models import  User

LOG =logging.getLogger(__name__)


class OrderApi(object):
    def __init__(self, db):
        self.db = db  # 数据库实例子

    def init_from_db(self, db):
        self.db = db

    @staticmethod
    def currency_exchange(hold_currency, hold_amount,
                          exchange_currency
                          ):
        if hold_currency == ECCHANGE_CURRENCY_TYPE['CNY'] \
                and exchange_currency ==  ECCHANGE_CURRENCY_TYPE['USD']:
            exchange_amount = hold_amount * 0.08
            return exchange_amount
        return 0

    @staticmethod
    def get_current_exchange_rate():
        return 0.08

    def get_maker_order_list(self, user_id, page, size):
        try:
            order_obj_list = self.db.session.query(MakerOrder).\
                filter(MakerOrder.user_id == user_id,
                       ~MakerOrder.status.in_(['complete','canceled'])).\
                limit(size).offset((page-1)*size)
            if order_obj_list:
                return order_obj_list
        except Exception:
            LOG.error(print_exc())
            return None

    def get_taker_order_list(self, user_id, page, size):
        try:
            order_obj_list = self.db.session.query(MakerOrder). \
                filter(TakerOrder.user_id == user_id,
                       ~TakerOrder.status.in_(['complete', 'canceled'])). \
                limit(size).offset((page - 1) * size)
            if order_obj_list:
                return order_obj_list
        except Exception:
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
            return maker_order_obj.id
        except Exception as e:
            self.db.session.rollback()
            LOG.error("xx"% print_exc())
        return None

    def update_taker_related_maker_order(self, book_no, stauts):
        try:
            obj = MakerOrder.query.filter_by(book_no=book_no).first()
            if obj:
                obj.status = stauts
            self.db.session.flush()
        except Exception as e:
            LOG.error("update related maker order err%s" % print_exc())

    def update_maker_related_taker_order(self, book_no, stauts):
        try:
            obj = TakerOrder.query.filter_by(book_no=book_no).first()
            if obj:
                obj.status = stauts
            self.db.session.flush()
        except Exception as e:
            LOG.error("update related maker order err%s" % print_exc())

    def create_taker_order(self, user_id, book_no, hold_currency,
                           hold_amount, exchange_currency,
                           exchange_amount, exchange_rate, status):
        try:
            now_time = int(time.time())
            taker_order_obj = TakerOrder(book_no=book_no,
                                         user_id=user_id,
                                         hold_currency=hold_currency,
                                         exchange_currency=exchange_currency,
                                         hold_amount=hold_amount,
                                         exchange_amount=exchange_amount,
                                         exchange_rate=exchange_rate,
                                         create_time=now_time,
                                         status=status)
            self.db.session.add(taker_order_obj)
            self.db.session.flush()
            return True
        except Exception as e:
            LOG.error("create taker order err%s" % print_exc())
            return False

    def update_taker_order(self, pk, status):
        try:
            obj = TakerOrder.query.filter_by(id=pk).first()
            if obj:
                obj.status = status
            self.db.session.flush()
        except Exception as e:
            LOG.error("create taker order err%s" % print_exc())

    def update_maker_order(self, pk, status):
        try:
            obj = MakerOrder.query.filter_by(id=pk).first()
            if obj:
                obj.status = status
            self.db.session.flush()
        except Exception as e:
            LOG.error("create taker order err%s" % print_exc())









