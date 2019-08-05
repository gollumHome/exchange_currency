# coding:utf-8
"""
description: 数据工具
author: jiangyx3915
date: 2019-05-22
"""
from apps.models import db
import copy


def model_to_json(query, fields=()):
    """
    模型 -> json
    :return:
    """
    if isinstance(query, db.Model):
        data = copy.deepcopy(query._sa_instance_state.dict)
        data.pop('_sa_instance_state')
        if fields:
            result = {}
            for field in fields:
                result[field] = data.get(field, '')
            return result
        return data
    return {}


def model_list_to_json(querys, fields=()):
    result = []
    for item in querys:
        result.append(model_to_json(item, fields))
    return result
