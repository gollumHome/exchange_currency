#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################
#   用户类
###############################################################

from traceback import print_exc
import time
import logging
from sqlalchemy import *
from apps.utils import Utils

from apps.models import  User
from apps.redis_client import RedisClient

redis_api = RedisClient()

logger =logging.getLogger(__name__)


class UserApi(object):
    def __init__(self, db):
        self.db = db

    def register(self, data):
        try:
            self.db.session.add(User(username=data['username'],
                                     head_url=data['head_url'],
                                     telephone=data['telephone'],
                                     email=data['email'],
                                     ID_verify=data['id_verify'],
                                     status=data['status'],
                                     Passport_verify=data['passport_verify'],
                                     verify_channel=data['verify_channel'],
                                     invite_code=data['invite_code'],
                                     additional_emails=data['additional_emails']))
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

