# -*- coding: utf-8 -*-
import unittest

test = unittest.TestCase()


def assert_list(expected, actual):
    test.assertEqual(len(expected), len(actual))
    for expected_data, actual_data in zip(expected, actual):
        if isinstance(expected_data, dict):
            assert_dict(expected_data, actual_data)
        else:
            test.assertEqual(expected_data, actual_data)


def assert_dict(expected, actual):
    for key, value in expected.items():
        if isinstance(value, dict):
            assert_dict(value, actual[key])
        elif isinstance(value, list):
            assert_list2(value, actual[key])
        else:
            test.assertEqual(value, actual[key])

def assert_list2(expected, actual):
    test.assertEqual(len(expected), len(actual))
    for expected_data, actual_data in zip(expected, actual):
        if isinstance(expected_data, dict):
            assert_dict(expected_data, actual_data)
        else:
            test.assertEqual(expected_data, actual_data)

class Expected:
    """
    新的效验类
    """
    def __init__(self, expected):
        self.expected = expected

    def validate(self, actual):
        if isinstance(actual, list):
            assert_list(self.expected, actual)

        elif isinstance(actual, dict):
            assert_dict(self.expected, actual)

        else:
            raise ValueError("Not support value")


def is_success_request(json_data):
    if not json_data:
        raise Exception("不能为空")
    if "code" not in json_data:
        raise Exception("json 没有 code")
    test.assertEqual(json_data["code"], "success", msg="请求失败 {}".format(json_data))


def is_error_request(json_data, err_msg):
    if not json_data:
        raise Exception("不能为空")
    if "code" not in json_data:
        raise Exception("json 没有 code")
    if "info" not in json_data:
        raise Exception("json 没有 info")
    test.assertEqual(json_data["code"], "error", msg="不是失败的请求 {}".format(json_data))
    test.assertEqual(json_data["info"], err_msg, msg="{} != {}".format(err_msg, json_data["info"]))