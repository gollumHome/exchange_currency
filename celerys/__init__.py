# -*- coding: utf-8 -*-

from celery import Celery


def create_celery():
    # 创建celery实例
    saas_api = Celery('saas-api')
    # 通过celery实例加载配置模块
    saas_api.config_from_object('celerys.celeryconfig')
    return saas_api
