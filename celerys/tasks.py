# -*- coding: utf-8 -*-

import os
import sys
from celerys import create_celery
from celery import platforms

from apps import create_app

from apps import db
from SchedulerService import SchedulerApi
from apps.PayService import PayApi

platforms.C_FORCE_ROOT = True
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()

celery = create_celery()

scheduler_api = SchedulerApi(db, sys.modules[__name__])

pay_api = PayApi(db)


@celery.task
def cycle_get_taker_order_job():
    with app.app_context():
        scheduler_api.monitor_maker_order(app)


@celery.task
def async_add_attend(user_id, activity_id):
    with app.app_context():
        pass


@celery.task
def cycle_get_token_job():
    with app.app_context():
        scheduler_api.get_access_token(app)


@celery.task
def settle_job():
    with app.app_context():
        pass



@celery.task
def recove_order_job():
    with app.app_context():
        scheduler_api.recove_timeout_order()



@celery.task
def query_wx_order_job():
    with app.app_context():
        scheduler_api.wx_order_query(app)



@celery.task
def reward_rank_job():
    with app.app_context():
        scheduler_api.reward_rank()


@celery.task
def complete_enrolls_job():
    with app.app_context():
        scheduler_api.complete_enrolls()



@celery.task
def recove_reward_job():
    with app.app_context():
        scheduler_api.recove_reward_order()



@celery.task
def complete_groups():
    with app.app_context():
        scheduler_api.complete_groups()



@celery.task
def close_timeout_activity():
    with app.app_context():
        scheduler_api.close_timeout_activity()



@celery.task
def remove_timeout_member():
    with app.app_context():
        scheduler_api.remove_timeout_member(app)



@celery.task
def enroll_statics():
    with app.app_context():
        scheduler_api.enroll_statics()

