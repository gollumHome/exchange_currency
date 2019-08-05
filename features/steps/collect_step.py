# -*- coding: utf-8 -*-
import json
import datetime
import time
import logging
from behave import *
from apps.models import Activity, Merchant, User, Courses

# from application import app

# logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@when("用户'{username}'收藏最近添加的活动")
def step_impl(context, username):
    with context.app.app_context():
        user = User.query.filter_by(nickname=username).first()
        activity = Activity.query.order_by(Activity.id.desc()).first()
        response = context.client.post(
            "/api/collect/",
            json={"activity_id": activity.id},
            headers={"Authorization": "JWT " + user.access_token},
        )

    context.bdd.is_success_request(response.json)


@when("用户'{username}'收藏最近添加的课程")
def step_impl(context, username):
    with context.app.app_context():
        user = User.query.filter_by(nickname=username).first()
        course = Courses.query.order_by(Courses.id.desc()).first()
        response = context.client.post(
            "/api/collect/",
            json={"course_id": course.id},
            headers={"Authorization": "JWT " + user.access_token},
        )

    context.bdd.is_success_request(response.json)


@then("用户'{username}'查询我的收藏")
def step_impl(context, username):
    with context.app.app_context():
        user = User.query.filter_by(nickname=username).first()
        response = context.client.get(
            "/api/collects/",
            headers={"Authorization": "JWT " + user.access_token},
        )
    expected_data = json.loads(context.text)
    context.bdd.is_success_request(response.json)
    actual_data = response.json["data"]
    expected = context.bdd.Expected(expected_data)
    expected.validate(actual_data)
