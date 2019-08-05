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


@when("'{merchant_name}'创建抽奖活动")
def step_impl(context, merchant_name):

    data = json.loads(context.text)
    data["finish_time"] = get_time(data["finish_time"])
    data["music_id"] = 1
    data["effect_id"] = 1
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=merchant_name).first()
        response = context.client.post(
            "/api/activity",
            json=data,
            headers={"Authorization": "JWT " + merchant.access_token},
        )
        context.bdd.is_success_request(response.json)



@then("商户'{username}'查看最近创建的抽奖活动")
def step_impl(context, username):
    with context.app.app_context():
        # user = User.query.filter_by(nickname=username).first()
        merchant = Merchant.query.filter_by(name=username).first()
        activity = Activity.query.order_by(Activity.id.desc()).first()
        activity_id = activity.id
        response = context.client.get(
            "/api/activity/lottery_merchant/{}/".format(activity_id),
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


@when("商家'{username}'更新抽奖活动")
def step_impl(context, username):
    with context.app.app_context():
        activity = Activity.query.order_by(Activity.id.desc()).first()
        merchant = Merchant.query.filter_by(name=username).first()
        json_data = json.loads(context.text)
        json_data["finish_time"] = get_time(json_data["finish_time"])
        json_data["music_id"] = 1
        json_data["effect_id"] = 1
        response = context.client.put(
            "/api/activity/lottery_merchant/{}/".format(activity.id),
            json=json_data,
            headers={"Authorization": "JWT " + merchant.access_token},
        )

        context.bdd.is_success_request(response.json)


@then("用户'{username}'查看最近创建的抽奖活动")
def step_impl(context, username):
    user = User.query.filter_by(nickname=username).first()
    activity = Activity.query.order_by(Activity.id.desc()).first()
    activity_id = activity.id
    response = context.client.get(
        "/api/activity/lottery/{}/".format(activity_id),
        headers={"Authorization": "JWT " + user.access_token},
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


@when("用户'{username}'在最近的抽奖活动中抽奖")
def step_impl(context, username):
    """
    没有报名的用户,需要先报名,才能抽奖
    """
    context.response = None
    with context.app.app_context():
        activity = Activity.query.order_by(Activity.id.desc()).first()
        user = User.query.filter_by(nickname=username).first()
        response = context.client.put(
            "/api/activity/lottery/{}/".format(activity.id),
            json={},
            headers={"Authorization": "JWT " + user.access_token},
        )
        # context.bdd.is_success_request(response.json)
    context.response = response.json


@then("用户'{username_a}'查看'{username_b}'share的抽奖活动")
def step_impl(context, username_a ,username_b):
    # with context.app.app_context():
    user_a = User.query.filter_by(nickname=username_a).first()
    user_b = User.query.filter_by(nickname=username_b).first()
    activity = Activity.query.order_by(Activity.id.desc()).first()
    activity_id = activity.id
    response = context.client.get(
        "/api/activity/lottery/{}/".format(activity_id),
        query_string={"user_id": user_b.id},
        headers={"Authorization": "JWT " + user_a.access_token},
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


@when("用户'{username_a}'给'{username_b}'最近参加的抽奖活动增加抽奖机会")
def step_impl(context, username_a, username_b):
    with context.app.app_context():
        context.response = None
        user_a = User.query.filter_by(nickname=username_a).first()
        user_b = User.query.filter_by(nickname=username_b).first()
        activity = Activity.query.order_by(Activity.id.desc()).first()
        activity_id = activity.id
        response = context.client.post(
            "/api/activity/lottery/{}/".format(activity_id),
            json={"user_id": user_b.id},
            headers={"Authorization": "JWT " + user_a.access_token},
        )
        context.response = response.json
        print("response.json=",response.json)