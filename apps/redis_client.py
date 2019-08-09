# -*- coding: utf-8 -*-

import logging
import redis
import json
from traceback import print_exc

logger = logging.getLogger()


class RedisClient:
    def __init__(self):
        self.pool = ""
        self.redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)
        self.MY_ASSIST_RANK = 'MY_ASSIST_RANK'

    # def init_from_app(self, app):
    #     self.redis_client = redis.Redis(host=app.config['REDIS_SERVER_HOST'], port=6379, db=0)

    def get_scribe_obj(self):
        return self.redis_client.pubsub()

    # key weiyi
    def set_scribe_expired(self, pk, expire_time):
        try:
            return self.redis_client.expire(pk, expire_time)
        except:
            logger.error(print_exc)

    def subscribe_set_keyvalues(self, key, value):
        try:
            return self.redis_client.set(key, value)
        except:
            logger.error(print_exc)
            return None

    def add_monitor_porcess_order(self, user, activity_id):
        try:
            assist_info_set = ''.join(['ASSIST_INFO_SET', '-', str(activity_id)])
            self.redis_client.sadd(assist_info_set, user)
        except:
            print_exc

    def zdd_assist_rank(self, assist_count, user_id, activity_id):
        try:
            my_assist_rank = ''.join([self.MY_ASSIST_RANK, '-', str(activity_id)])
            self.redis_client.zadd(my_assist_rank, str(user_id), assist_count)
        except:
            print_exc

    def get_my_assist_rank(self, user_id, activity_id):
        try:
            my_assist_rank = ''.join([self.MY_ASSIST_RANK, '-', str(activity_id)])
            return self.redis_client.zrevrank(my_assist_rank, str(user_id)) + 1
        except:
            print_exc
            return 0

    def sadd_assist_user(self, user, activity_id):
        try:
            assist_info_set = ''.join(['ASSIST_INFO_SET', '-', str(activity_id)])
            self.redis_client.sadd(assist_info_set, user)
        except:
            print_exc

    def get_assist_set(self, activity_id, offset, limit):
        end_index = offset * limit + limit
        try:
            assist_info_set = ''.join(['ASSIST_INFO_SET', '-', str(activity_id)])

            results = list(self.redis_client.smembers(assist_info_set))
            print(results)
            length = self.redis_client.scard(assist_info_set)
            print(length)
            if offset > length:
                offset = 0
            if end_index > length:
                end_index = length
            results = results[offset:end_index]
            print(results)
            return length, [eval(x.decode('utf-8')) for x in results]
        except:
            print_exc(limit=5)
        return 0, None

    def sadd_envelope_user(self, user, activity_id):
        try:
            envelope_attend_set = ''.join(['ENVELOPE_ATTEND_SET', '-', str(activity_id)])
            self.redis_client.sadd(envelope_attend_set, user)
        except:
            print_exc

    def get_envelope_set(self, activity_id, offset, limit):
        end_index = offset*limit + limit
        try:
            envelope_attend_set = ''.join(['ENVELOPE_ATTEND_SET', '-', str(activity_id)])

            results = list(self.redis_client.smembers(envelope_attend_set))
            print(results)
            length = self.redis_client.scard(envelope_attend_set)
            print(length)
            if offset > length:
                offset = 0
            if end_index > length:
                end_index = length
            results = results[offset:end_index]
            print(results)
            return length, [eval(x.decode('utf-8')) for x in results]
        except:
            print_exc(limit=5)
        return 0, None
