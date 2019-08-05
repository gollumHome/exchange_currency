# -*- coding: utf-8 -*-
import json
import datetime
import time
import logging
from behave import *
from apps.models import Activity, Merchant, User


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_time(day):
    if "明天" == day:
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        now_time = tomorrow.strftime("%Y-%m-%d 00:00:00")
        tomorrow_ = datetime.datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S")
        un_time = int(time.mktime(tomorrow_.timetuple()))
    return un_time


@when("'{merchant_name}'创建微报名活动")
def step_impl(context, merchant_name):

    data = json.loads(context.text)
    data["finish_time"] = get_time(data["finish_time"])
    data["music_id"] = 1
    data["effect_id"] = 1
    data["type"] = "microEnroll"
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=merchant_name).first()
        response = context.client.post(
            "/api/activity",
            json=data,
            headers={"Authorization": "JWT " + merchant.access_token},
        )
        context.bdd.is_success_request(response.json)



@then("商户'{username}'查看最近创建的微报名活动")
def step_impl(context, username):
    with context.app.app_context():
        # user = User.query.filter_by(nickname=username).first()
        merchant = Merchant.query.filter_by(name=username).first()
        activity = Activity.query.order_by(Activity.id.desc()).first()
        activity_id = activity.id
        response = context.client.get(
            "/api/activity/micro_enroll_merchant/{}/".format(activity_id),
            headers={"Authorization": "JWT " + merchant.access_token},
        )
        expected_data = json.loads(context.text)
        expected = context.bdd.Expected(expected_data)
        actual_data = response.json["data"]
        logging.info(actual_data)
        expected_data["finish_time"] = get_time(expected_data["finish_time"])
        if actual_data["music"]:
            actual_data["music"] = actual_data["music"]["name"]
        if actual_data["effect"]:
            actual_data["effect"] = actual_data["effect"]["name"]
        expected.validate(actual_data)


@when("商家'{username}'修改最近的微报名活动")
def step_impl(context, username):

    with context.app.app_context():
        activity = Activity.query.order_by(Activity.id.desc()).first()
        merchant = Merchant.query.filter_by(name=username).first()
        json_data = json.loads(context.text)
        json_data["finish_time"] = get_time(json_data["finish_time"])
        json_data["music_id"] = 1
        json_data["effect_id"] = 1
        response = context.client.put(
            "/api/activity/micro_enroll_merchant/{}/".format(activity.id),
            json=json_data,
            headers={"Authorization": "JWT " + merchant.access_token},
        )

        context.bdd.is_success_request(response.json)


@then("用户'{username}'查看最近的微报名活动")
def step_impl(context, username):
    with context.app.app_context():
        user = User.query.filter_by(nickname=username).first()
        activity = Activity.query.order_by(Activity.id.desc()).first()
        activity_id = activity.id
        response = context.client.get(
            "/api/activity/micro_enroll/{}/".format(activity_id),
            headers={"Authorization": "JWT " + user.access_token},
        )
        expected_data = json.loads(context.text)
        expected = context.bdd.Expected(expected_data)
        actual_data = response.json["data"]
        expected_data["finish_time"] = get_time(expected_data["finish_time"])
        if actual_data["music"]:
            actual_data["music"] = actual_data["music"]["name"]
        if actual_data["effect"]:
            actual_data["effect"] = actual_data["effect"]["name"]
        expected.validate(actual_data)


@when("用户'{user_name}'报名最近的微报名活动")
def step_impl(context, user_name):
    with context.app.app_context():
        user = User.query.filter_by(nickname=user_name).first()
        activity = Activity.query.filter_by().order_by(Activity.id.desc()).first()
        json_data = json.loads(context.text)
        json_data["product_id"] = activity.id
        json_data["product_type"] = "course"
        response = context.client.post(
            "/api/enroll/".format(activity.id),
            json=json_data,
            headers={"Authorization": "JWT " + user.access_token},
        )
    logging.info(response.json)
    context.bdd.is_success_request(response.json)