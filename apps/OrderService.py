#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################
#   订单服务类
###############################################################

from traceback import print_exc
import time
import uuid
from sqlalchemy import *
from apps.utils import Utils

from apps.models import Orders, User, Activity, Merchant, Courses, Enroll


class OrderApi(object):
    def __init__(self, db):
        self.db = db  # 数据库实例子

    def init_from_db(self, db):
        self.db = db

    def get_order_by_no(self, order_no,order_type):
        try:
            if order_type == 'member':
                  order_obj = self.db.session.query(Orders.id, Orders.order_no, Orders.product_id, Orders.title,
                                                    Orders.user_id, Orders.merchant_id, Orders.user_id, Orders.shares,
                                                    Orders.price, Orders.img_url, Orders.order_amount,Orders.status,Orders.finish_time,Orders.create_time,Merchant.organization_name,Merchant.telephone)\
                        .filter(Orders.order_no == order_no) \
                        .join(Merchant, Merchant.id == Orders.user_id).first()
            else:
                order_obj = self.db.session.query(Orders.id, Orders.order_no, Orders.product_id,
                                                  Orders.title,
                                                  Orders.user_id, Orders.merchant_id, Orders.user_id,
                                                  Orders.shares,
                                                  Orders.price, Orders.img_url, Orders.order_amount,
                                                  Orders.status, Orders.finish_time, Orders.create_time,
                                                  User.nickname, User.head_url) \
                    .filter(Orders.order_no == order_no) \
                    .join(User, User.id == Orders.user_id).first()
            return order_obj
        except:
            print_exc()
        return None

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

    def create_order(self, user_id, merchant_id, product_id,
                     title, shares, img_url, price, order_amount, attach, order_type,enroll_id):

        if order_type in ['activity', 'course'] and not self.check_inventory(order_type, product_id, shares):
            return {"code": "error", "info": "库存不足"}
        now_time = int(time.time())
        status = 'prepay'
        order_no = Utils.get_system_no()
        try:
            order_obj = Orders(user_id=user_id, order_no=order_no, product_id=product_id, merchant_id=merchant_id,
                               title=title, shares=shares, img_url=img_url, price=price,  order_amount=order_amount,
                               create_time=now_time, attach=attach, order_type=order_type, status=status)
            self.db.session.add(order_obj)
            self.db.session.flush()
            if order_type in ['activity', 'course']:
                enroll_info = Enroll.query.filter(Enroll.id == enroll_id).first()
                enroll_info.order_id = order_obj.id
            self.db.session.commit()
            return {"code": "success", "order_no": order_no}
        except:
            self.db.session.rollback()
            print_exc()
        return {"code": "error", "info": "订单生产异常"}

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
