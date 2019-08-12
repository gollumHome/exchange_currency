# coding:utf-8
"""
description: 文件工具
author: jiangyx3915
date: 2019-05-22
"""
from apps import (
    tc_oss,
    utils
)


def upload_file_to_oss(file) -> dict:
    """
    上传文件至oss
    :param file:
    :return: bool
    """
    result = {}
    img_name = utils.Utils.get_system_no()
    file_ext = file.filename.rsplit('.', 1)[1]
    if file:
        try:
            file_bytes = file.read()
            img_name = img_name + "." + file_ext
            img_url = tc_oss.upload_image(img_name, file_bytes)
            result.update({'name': img_name, 'url': img_url})
        except Exception:
            return result
    return result
