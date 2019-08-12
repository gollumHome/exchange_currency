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















