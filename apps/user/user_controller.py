#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################
#   用户类
###############################################################

from traceback import print_exc
import random
import time
import string
import logging
from sqlalchemy import *
from apps.utils import md5
from apps.constant import REWARD_AMOUT

from apps.models import *
from apps.redis_client import RedisClient

redis_api = RedisClient()

logger =logging.getLogger(__name__)


class UserApi(object):
    def __init__(self, db):
        self.db = db

    def invite_recrod(self, data):
        try:
            user = self.db.session.query(User).filter(User.invite_code\
                                                      ==data['invite_code']).first()
            if not user:
                raise Exception
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 32))
            self.db.session.add(UserReward(
                amount=REWARD_AMOUT,
                user_id=user.id,
                password=md5(data['password'], salt),
                email=data['email'],
                share_id=data['invite_code'],
                create_time=int(time.time()),
                status=data['status']))
            self.db.session.flush()
            return True
        except Exception:
            logger.error(print_exc())
            return False

    def register(self, data):
        try:
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 32))
            self.db.session.add(User(
                                     salt=salt,
                                     password=md5(data['password'], salt),
                                     email=data['email'],
                                     invite_code=data['invite_code'],
                                     status=data['status']))
            self.db.session.flush()
            return True
        except Exception:
            logger.error(print_exc())
            return False

    def update_user_password(self, user, new_password):
        try:
            user.password = md5(new_password, user.salt)
            self.db.session.commit()
            return True
        except Exception:
            logger.error(print_exc())
            return False

    def logout(self, user_id):
        user = User.query.filter(User.id == int(user_id)).first()
        if user:
            redis_api.remove_user_token(user.access_token)
            return True
        else:
            return False

    def loginIn(self, password,salt):
        if password != md5(password, salt):
            return False
        return True

    def get_invite_recrod_list(self,user_id, page, size):
        try:
            recrod_obj_list = self.db.session.query(UserReward).\
                filter(TakerOrder.user_id == user_id).\
                limit(size).offset((page - 1) * size)
            if recrod_obj_list:
                return recrod_obj_list
        except Exception:
            logger.error(print_exc())
            return None
