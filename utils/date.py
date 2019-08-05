# coding:utf-8
"""
description: 日期工具
author: jiangyx3915
date: 2019-05-23
"""
import time


def get_target_date_timestamp(date: str) -> int:
    """
    获取指定日期的时间戳
    :param date:
    :return:
    """
    if not date:
        return 0
    time_array = time.strptime(date, "%Y-%m-%d")
    return int(time.mktime(time_array))
