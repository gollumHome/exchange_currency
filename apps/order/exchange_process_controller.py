# coding: utf-8

import logging
from traceback import print_exc
from apps.models import *
import time
from decimal import Decimal
from .constant import TAKER_ORDER_STATUS,EXCHANGE_PROCESS_STATUS

from apps.tencent_sms import TencentSms

LOG =logging.getLogger(__name__)


class ProcesApi(object):
    def __init__(self, db):
        self.db = db

    def init_from_db(self, db):
        self.db = db

    def create_exchange_process(self, book_no,
                                user_id,
                                status,
                                entrust_type):
        try:
            expire_time = 0
            now_time = int(time.time())
            if status == '':
                expire_time = now_time = 30
            if status == '':
                expire_time = now_time = 30
            taker_order_obj = ExchangeProgres(book_no=book_no,
                                              user_id=user_id,
                                              status=status,
                                              create_time=now_time,
                                              expire_time=expire_time,
                                              entrust_type=1)
            self.db.session.add(taker_order_obj)
            self.db.session.flush()
            return True
        except Exception as e:
            LOG.error("create taker order err%s" % print_exc())
            return False

    def update_exchange_process(self, pk, stauts):
        try:
            obj = ExchangeProgres.query.filter_by(id=pk).first()
            resp_data = dict()
            if obj:
                if obj.status == TAKER_ORDER_STATUS['matched']:
                    expire_time = int(time.time()) + 30
                if obj.status == TAKER_ORDER_STATUS['set_wallet']:
                    expire_time = int(time.time()) + 30
                    service_fee = self.confirm_service_charge(obj.book_no,
                                                              obj.entrust_type)
                    obj.status = stauts
                    obj.expire_time = expire_time
                    resp_data['status'] = TAKER_ORDER_STATUS['set_wallet']
                    resp_data['service_fee'] = service_fee
            self.db.session.commit()
            return resp_data
        except Exception as e:
            self.db.session.rollback()
            LOG.error("update exchange process  err%s" % print_exc())
            return {}

    def update_taker_related_porcess(self, book_no, entrust_type, status):
        try:
            obj =ExchangeProgres.query.filter_by(book_no=book_no,
                                                 entrust_type=entrust_type).first()
            if obj:
                obj.status = status
            self.db.session.flush()
            return True
        except Exception as e:
            LOG.error("update related maker order err%s" % print_exc())
            return False

    def confirm_service_charge(self, book_no, entrust_type):
        try:
            obj = TakerOrder.query.filter_by(book_no=book_no,
                                             entrust_type=entrust_type).first()

            if obj:
                fee_count = self.calculate_currency_charge(obj.hold_currency,
                                               obj.exchange_currency,
                                               obj.book_no)
                return fee_count
        except Exception as e:
            self.db.session.rollback()
            LOG.error("update exchange process  err%s" % print_exc())
            return 0

    def calculate_currency_charge(self,hold_currency,
                                  exchange_currency,
                                  exchange_amount):
        if hold_currency == '' and exchange_currency == '':
            value = Decimal(str(exchange_amount)).quantize(Decimal('0.00'))
            return '{0:^8}'.format(value)

    # monitor process whetheater expired
    def motior_process_task(self, key):
        pass

    def add_exchange_wallet(self, pk, data):
        try:
            obj = ExchangeProgres.query.filter_by(id=pk).first()
            if obj:
                obj.status = EXCHANGE_PROCESS_STATUS['set_wallet']
                obj.extend_remark = data
            self.db.session.flush()
            return True
        except Exception as e:
            LOG.error("create taker order err%s" % print_exc())
            return False

    def get_exchange_process_obj(self,book_no,entrust_type):
        try:
            obj = ExchangeProgres.query.filter_by(book_no=book_no,
                                                  entrust_type=entrust_type).first()
            if obj:
               return obj
        except Exception as e:
            LOG.error("create taker order err%s" % print_exc())
            return None
