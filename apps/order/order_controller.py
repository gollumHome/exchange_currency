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
from apps.models import  User, Activity, Merchant, Courses, Enroll

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

    def get_orders_by_userid(self, user_id, status_list, offset, limit, order_type):
        try:
            if status_list:
                    if order_type:
                            order_list = self.db.session.query(Orders.id, Orders.order_no, Orders.product_id,
                                                               Orders.title, Orders.merchant_id, Orders.user_id, Orders.product_num,
                                                               Orders.price, Orders.show_price, Orders.img_url, Orders.order_amount, Orders.status,Orders.finish_time,Orders.create_time,User.nickname,User.head_url)\
                                .filter(and_(Orders.user_id == user_id, Orders.order_type == order_type))\
                                .filter(Orders.status.in_(tuple(status_list)))\
                                .join(User, User.id == Orders.merchant_id).order_by(desc(Orders.create_time)).limit(limit).offset(offset)
                    else:
                            order_list = self.db.session.query(Orders.id, Orders.order_no, Orders.product_id, Orders.title,
                                                               Orders.merchant_id, Orders.user_id, Orders.product_num,
                                                               Orders.price, Orders.show_price, Orders.img_url, Orders.order_amount,Orders.status,Orders.finish_time,Orders.create_time,User.nickname,User.head_url)\
                                .filter(Orders.user_id == user_id)\
                                .filter(Orders.status.in_(tuple(status_list)))\
                                .join(User, User.id == Orders.merchant_id).order_by(desc(Orders.create_time)).limit(limit).offset(offset)
            else:
                if order_type:
                    order_list = self.db.session.query(Orders.id, Orders.order_no, Orders.product_id, Orders.title,
                                                       Orders.merchant_id, Orders.user_id, Orders.product_num,
                                                       Orders.price, Orders.show_price, Orders.img_url, Orders.order_amount,Orders.status,Orders.finish_time,Orders.create_time,User.nickname,User.head_url)\
                        .filter(and_(Orders.user_id == user_id,Orders.order_type == order_type)) \
                        .join(User, User.id == Orders.merchant_id).order_by(desc(Orders.create_time)).limit(limit).offset(offset)
                else:
                    order_list = self.db.session.query(Orders.id, Orders.order_no, Orders.product_id, Orders.title,
                                                          Orders.merchant_id, Orders.user_id, Orders.product_num,
                                                          Orders.price, Orders.show_price, Orders.img_url, Orders.order_amount,Orders.status,Orders.finish_time,Orders.create_time,User.nickname,User.head_url)\
                        .filter(Orders.user_id == user_id) \
                        .join(User, User.id == Orders.merchant_id).order_by(desc(Orders.create_time)).limit(limit).offset(offset)

            return order_list
        except:
            print_exc()
        return None

    def get_orders_by_merchantid(self, merchant_id, status_list, offset, limit, order_type):
        try:
            if status_list:
                    if order_type:
                            order_list = self.db.session.query(Orders.id, Orders.order_no, Orders.product_id, Orders.title,
                                                          Orders.merchant_id, Orders.user_id, Orders.product_num,
                                                          Orders.price,Orders.show_price,  Orders.img_url, Orders.order_amount,Orders.status,Orders.finish_time,Orders.create_time,User.nickname,User.head_url)\
                                .filter(Orders.merchant_id == merchant_id)\
                                .filter(Orders.status.in_(tuple(status_list)))\
                                .filter(Orders.order_type == order_type)\
                                .join(User, User.id == Orders.user_id).order_by(desc(Orders.create_time)).limit(limit).offset(offset)
                    else:
                            order_list = self.db.session.query(Orders.id, Orders.order_no, Orders.product_id, Orders.title,
                                                          Orders.merchant_id, Orders.user_id, Orders.product_num,
                                                          Orders.price, Orders.show_price, Orders.img_url, Orders.order_amount,Orders.status,Orders.finish_time,Orders.create_time,User.nickname,User.head_url)\
                                .filter(Orders.merchant_id == merchant_id)\
                                .filter(Orders.status.in_(tuple(status_list)))\
                                .join(User, User.id == Orders.user_id) .order_by(desc(Orders.create_time)).limit(limit).offset(offset)
            else:
                if order_type:
                            order_list = self.db.session.query(Orders.id, Orders.order_no, Orders.product_id, Orders.title,
                                                          Orders.merchant_id, Orders.user_id, Orders.product_num,
                                                          Orders.price,Orders.show_price,  Orders.img_url, Orders.order_amount,Orders.status,Orders.finish_time,Orders.create_time,User.nickname,User.head_url)\
                        .filter(Orders.merchant_id == merchant_id)\
                        .filter(Orders.order_type == order_type)\
                        .join(User, User.id == Orders.user_id).order_by(desc(Orders.create_time)).limit(limit).offset(offset)
                else:
                    order_list = self.db.session.query(Orders.id, Orders.order_no, Orders.product_id, Orders.title,
                                                          Orders.merchant_id, Orders.user_id, Orders.product_num,
                                                          Orders.price, Orders.show_price, Orders.img_url, Orders.order_amount,Orders.status,Orders.finish_time,Orders.create_time,User.nickname,User.head_url)\
                        .filter(Orders.merchant_id == merchant_id)\
                        .join(User, User.id == Orders.user_id).order_by(desc(Orders.create_time)).limit(limit).offset(offset)

            return order_list
        except:
            print_exc()
        return None



    # 检查库存剩余
    def check_inventory(self, order_type, product_id, shares):
        if order_type == 'activity':
            product = Activity.query.filter(Activity.id == product_id).first()
            inventory = product.inventory
        else:
            product = Courses.query.filter(Courses.id == product_id).first()
            inventory = product.count

        order_list = Orders.query.filter(and_(Orders.product_id == product_id, Orders.order_type == order_type,
                                              or_(Orders.status == 'payed', Orders.status == 'paying', Orders.status == 'complete', Orders.status == 'prepay'))).all()
        locked_num = sum([order.shares for order in order_list]) if order_list else 0
        return inventory >= (shares + locked_num)

    # 查询库存剩余
    def get_inventory(self, product_id, order_type):
        if order_type == 'activity':
            product = Activity.query.filter(Activity.id == product_id).first()
        else:
            product = Courses.query.filter(Courses.id == product_id).first()
        inventory = product.inventory
        order_list = Orders.query.filter(and_(Orders.product_id == product_id, Orders.order_type == order_type,
                                              or_(Orders.status == 'payed', Orders.status == 'paying',
                                                  Orders.status == 'complete', Orders.status == 'prepay'))).all()
        locked_num = sum([order.shares for order in order_list]) if order_list else 0
        return inventory - locked_num

    def update_order_paying(self, order_no, prepay_id):
        order_obj = Orders.query.filter(Orders.order_no == order_no).first()
        order_obj.prepay_id = prepay_id
        order_obj.status = 'paying'
        self.db.session.commit()
