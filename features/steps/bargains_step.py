# -*- coding: utf-8 -*-
import json
import datetime
import time
import logging
from behave import *
from apps.models import Activity, Merchant, User

# from application import app

# logger = logging.getLogger(__name__)
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


@when("'{merchant_name}'创建砍价活动")
def step_impl(context, merchant_name):

    data = json.loads(context.text)
    data["finish_time"] = get_time(data["finish_time"])
    data["music_id"] = 1
    data["effect_id"] = 1
    data['extra_fields'] = data["settings"]
    data["type"] = "bargain"
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=merchant_name).first()
        response = context.client.post(
            "/api/activity",
            json=data,
            headers={"Authorization": "JWT " + merchant.access_token},
        )
        context.bdd.is_success_request(response.json)


@then("用户'{username}'查看最近创建的砍价活动")
def step_impl(context, username):
    with context.app.app_context():
        user = User.query.filter_by(nickname=username).first()
        activity = Activity.query.order_by(Activity.id.desc()).first()
        activity_id = activity.id
        response = context.client.get(
            "/api/activity/bargain/{}/".format(activity_id),
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

#
# @then("用户'{username1}'查看'{username2}'分享的砍价支付活动")
# def step_impl(context, username1, username2):
#     with context.app.app_context():
#         user1 = User.query.filter_by(nickname=username1).first()
#         user2 = User.query.filter_by(nickname=username2).first()
#
#         activity = Activity.query.order_by(Activity.id.desc()).first()
#         activity_id = activity.id
#         response = context.client.get(
#             "/api/activity/bargain_with_pay/{}/".format(activity_id),
#             query_string={"user_id": user2.id},
#             headers={"Authorization": "JWT " + user1.access_token},
#         )
#         expected_data = json.loads(context.text)
#         expected = context.bdd.Expected(expected_data)
#         actual_data = response.json["data"]
#         # logging.info("dadta=", response.json["data"])
#         expected_data["finish_time"] = get_time(expected_data["finish_time"])
#
#         # logging.info(actual_data["music"])
#         if actual_data["music"]:
#             actual_data["music"] = actual_data["music"]["name"]
#         if actual_data["effect"]:
#             actual_data["effect"] = actual_data["effect"]["name"]
#
#         expected.validate(actual_data)
#
#
# @when("用户'{username}'参加最近添加的砍价活动")
# def step_impl(context, username):
#     with context.app.app_context():
#         context.response = None
#         user = User.query.filter_by(nickname=username).first()
#         activity = Activity.query.order_by(Activity.id.desc()).first()
#         response = context.client.post(
#             "/api/activity/bargain_with_pay/{}/".format(activity.id),
#             headers={"Authorization": "JWT " + user.access_token},
#             json={}
#         )
#
#         logging.info(response.json)
#         assert "code" in response.json
#         context.response = response.json
#
#
#
# @when("用户'{username1}'帮'{username2}'砍价")
# def step_impl(context, username1, username2):
#
#     with context.app.app_context():
#         context.response = None
#         user1 = User.query.filter_by(nickname=username1).first()
#         user2 = User.query.filter_by(nickname=username2).first()
#         activity = Activity.query.order_by(Activity.id.desc()).first()
#         response = context.client.post(
#             "/api/activity/bargain_item_with_pay/{}/?user_id={}".format(activity.id, user2.id),
#             headers={"Authorization": "JWT " + user1.access_token},
#             json={}
#         )
#         context.response = response.json
#
#
# @then("查看'{username}'砍价支付的详情")
# def step_impl(context, username):
#     with context.app.app_context():
#         user = User.query.filter_by(nickname=username).first()
#         bargain = Bargains.query.order_by(Bargains.id.desc()).first()  # type: Bargains
#         response = context.client.get(
#             "/api/activity/bargain_item_with_pay/{}/".format(bargain.activity_id),
#             query_string={"user_id": user.id}
#         )
#     expected_data = json.loads(context.text)
#     context.bdd.is_success_request(response.json)
#     actual_data = response.json["data"]
#     expected = context.bdd.Expected(expected_data)
#     expected.validate(actual_data)
#
#
#
# @then("商家'{username}'查看最近的砍价支付活动")
# def step_impl(context, username):
#     with context.app.app_context():
#         activity = Activity.query.order_by(Activity.id.desc()).first()
#         merchant = Merchant.query.filter_by(name=username).first()
#         response = context.client.get(
#             "/api/activity/bargain_with_pay_merchant/{}/".format(activity.id),
#             headers={"Authorization": "JWT " + merchant.access_token},
#         )
#
#     expected_data = json.loads(context.text)
#     expected_data["finish_time"] = get_time(expected_data["finish_time"])
#     context.bdd.is_success_request(response.json)
#     actual_data = response.json["data"]
#     if actual_data["music"]:
#         actual_data["music"] = actual_data["music"]["name"]
#     if actual_data["effect"]:
#         actual_data["effect"] = actual_data["effect"]["name"]
#     expected = context.bdd.Expected(expected_data)
#     expected.validate(actual_data)
#
#
# @when("商家'{username}'修改最近的砍价支付活动")
# def step_impl(context, username):
#     with context.app.app_context():
#         activity = Activity.query.order_by(Activity.id.desc()).first()
#         merchant = Merchant.query.filter_by(name=username).first()
#         json_data = json.loads(context.text)
#         json_data["finish_time"] = get_time(json_data["finish_time"])
#         json_data["music_id"] = 1
#         json_data["effect_id"] = 1
#         response = context.client.put(
#             "/api/activity/bargain_with_pay_merchant/{}/".format(activity.id),
#             json=json_data,
#             headers={"Authorization": "JWT " + merchant.access_token},
#         )
#
#         context.bdd.is_success_request(response.json)
