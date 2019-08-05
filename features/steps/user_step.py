# -*- coding: utf-8 -*-
import time
import json
from behave import *
from apps.models import Music, Effects, db, Member, Merchant, User, Reservation, Courses, TelVerifyCode, Activity
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@when("用户'{user_name}'设置信息")
def step_impl(context, user_name):
    with context.app.app_context():
        user = User.query.filter_by(nickname=user_name).first()
        response = context.client.put(
            "/api/user/user/",
            json=json.loads(context.text),
            headers={"Authorization": "JWT " + user.access_token},
        )
    context.bdd.is_success_request(response.json)


@then("'{user_name}'得到自己的信息")
def step_impl(context, user_name):
    with context.app.app_context():
        user = User.query.filter_by(nickname=user_name).first()
        response = context.client.get(
            "/api/user/user/",
            headers={"Authorization": "JWT " + user.access_token},
        )
        expected_data = json.loads(context.text)
        expected = context.bdd.Expected(expected_data)
        logging.info(response.json)
        expected.validate(response.json["data"])


@when("用户'{user_name}'设置手机号码")
def step_impl(context, user_name):
    with context.app.app_context():
        context.response = None
        user = User.query.filter_by(nickname=user_name).first()
        json_data = json.loads(context.text)
        json_data["code"] = "1111"
        response = context.client.put(
            "/api/user/phone/",
            json=json_data,
            headers={"Authorization": "JWT " + user.access_token},
        )
        context.response = response.json


    assert "code" in response.json
    # context.bdd.is_success_request(response.json)

@when("用户'{user_name}'发送'{phone}'验证码")
def step_impl(context, user_name, phone):
    with context.app.app_context():
        user = User.query.filter_by(nickname=user_name).first()
        telVerifyInfo = TelVerifyCode(telephone=phone, verifyCode="1111",
                                   verify_type='add_phone')
        db.session.add(telVerifyInfo)
        db.session.commit()

@then("用户'{user_name}'查询自己报名的活动")
def step_impl(context, user_name):
    with context.app.app_context():
        user = User.query.filter_by(nickname=user_name).first()

        response = context.client.get(
            "api/user/activitys/",

            headers={"Authorization": "JWT " + user.access_token},
        )

        expected_data = json.loads(context.text)
        expected = context.bdd.Expected(expected_data)
        logging.info(response.json)
        expected.validate(response.json["data"])

    context.bdd.is_success_request(response.json)


# @when("用户'{user_name}'购买最近添加的课程")
# def step_impl(context, user_name):
#     with context.app.app_context():
#         user = User.query.filter_by(nickname=user_name).first()
#         course = Courses.query.filter_by().order_by(Courses.id.desc()).first()
#
#         response = context.client.post(
#             "/course/course/{}/".format(course.id),
#             json=json.loads(context.text),
#             headers={"Authorization": "JWT " + user.access_token},
#         )
#
#     context.bdd.is_success_request(response.json)

@when("用户'{user_name}'报名最近添加的课程")
def step_impl(context, user_name):
    with context.app.app_context():
        user = User.query.filter_by(nickname=user_name).first()
        activity = Courses.query.filter_by().order_by(Courses.id.desc()).first()
        json_data = json.loads(context.text)
        json_data["product_id"] = activity.id
        json_data["activity_type"] = "course"
        response = context.client.post(
            "/api/enroll/".format(activity.id),
            json=json_data,
            headers={"Authorization": "JWT " + user.access_token},
        )
    logging.info(response.json)
    context.bdd.is_success_request(response.json)


@then("用户'{username}'查询自己报名的课程")
def step_impl(context, username):
    with context.app.app_context():
        user = User.query.filter_by(nickname=username).first()

        response = context.client.get(
            "/api/user/courses/",
            headers={"Authorization": "JWT " + user.access_token},
        )

        expected_data = json.loads(context.text)
        expected = context.bdd.Expected(expected_data)
        logging.info(response.json)
        expected.validate(response.json["data"])

    context.bdd.is_success_request(response.json)


# @when("用户'{user_name}'购买最近添加的活动")
# def step_impl(context, user_name):
#     with context.app.app_context():
#         user = User.query.filter_by(nickname=user_name).first()
#         activity = Activity.query.filter_by().order_by(Activity.id.desc()).first()
#
#         response = context.client.put(
#             "/api/activity/bargain_with_pay/{}/".format(activity.id),
#             json=json.loads(context.text),
#             headers={"Authorization": "JWT " + user.access_token},
#         )
#
#     context.bdd.is_success_request(response.json)

@when("用户'{user_name}'报名最近添加的活动")
def step_impl(context, user_name):
    with context.app.app_context():
        user = User.query.filter_by(nickname=user_name).first()
        activity = Activity.query.filter_by().order_by(Activity.id.desc()).first()
        json_data = json.loads(context.text)
        json_data["product_id"] = activity.id
        json_data["activity_type"] = activity.activity_types
        response = context.client.post(
            "/api/enroll/".format(activity.id),
            json=json_data,
            headers={"Authorization": "JWT " + user.access_token},
        )
    logging.info(response.json)
    context.bdd.is_success_request(response.json)


@then("商户'{name}'查看课程订单")
def step_impl(context, name):
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=name).first()
        response = context.client.get(
            "/course/orders/",
            headers={"Authorization": "JWT " + merchant.access_token},
        )
        expected_data = json.loads(context.text)
        expected = context.bdd.Expected(expected_data)
        logging.info(response.json)
        expected.validate(response.json["data"])

    context.bdd.is_success_request(response.json)