# coding:utf-8
"""
description: 响应工具
author: jiangyx3915
date: 2019-05-22
"""
from flask import jsonify, Response


def response(code: str, info: str, data: dict, **extra) -> Response:
    """
    基础返回
    :param code:    响应码
    :param info:    响应信息
    :param data:    响应数据
    :return:
    """
    ret = {'code': code, 'info': info, 'data': data}
    ret.update(extra)
    return jsonify(ret)


def success_response(info: str = '', data=None, **extra) -> Response:
    """
    成功返回
    :param info:
    :param data:
    :return:
    """
    if data is None:
        data = {}
    return response('success', info, data, **extra)


def fail_response(info: str, data=None, **extra) -> Response:
    """
    失败返回
    :param info:
    :param data:
    :return:
    """
    if data is None:
        data = {}
    return response('error', info, data, **extra)
