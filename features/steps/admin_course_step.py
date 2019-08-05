# -*- coding: utf-8 -*-
import json
import datetime
import time
import logging
from behave import *
from apps.models import Activity, Merchant, User, Courses, AdminUser

# from application import app

# logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)



@when("管理员设置查询课程条件")
def step_impl(context):
    """设置条件
    context.filter_data
    :param context:
    :return:
    """
    json_data = json.loads(context.text)
    context.filter_data = json_data


@then("管理员'{username}'得到查询结果")
def step_impl(context, username):

    assert getattr(context, "filter_data")
    expected_data = json.loads(context.text)
    with context.app.app_context():

        admin_user = AdminUser.query.filter_by(nickname=username).first()
        response = context.client.get(
            "/platform/courses/", query_string=context.filter_data,
            headers={"Authorization": "JWT " + admin_user.access_token},
        )
        del context.filter_data
        context.bdd.is_success_request(response.json)
        actual_data = response.json["data"]
        expected = context.bdd.Expected(expected_data)
        expected.validate(actual_data)


@when("管理员'{username}'下架最新添加的课程")
def step_impl(context, username):
    with context.app.app_context():
        admin_user = AdminUser.query.filter_by(nickname=username).first()
        course = Courses.query.order_by(Courses.id.desc()).first()
        response = context.client.patch(
            "/platform/course/{}/".format(course.id),
            json={"status": "lower"},
            headers={"Authorization": "JWT " + admin_user.access_token},
        )

    context.bdd.is_success_request(response.json)