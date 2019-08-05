# -*- coding: utf-8 -*-
import time
import json
from behave import *
from apps.models import Music, Effects, db, Member, Merchant, User, Courses, Orders
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@when("商户'{merchant_name}'添加课程")
def step_impl(context, merchant_name):
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=merchant_name).first()
        req = context.client.post(
            "/course/add_course/",
            json=json.loads(context.text),
            headers={"Authorization": "JWT " + merchant.access_token},
        )
    logging.info(req)
    context.bdd.is_success_request(req.json)


@then("查看刚刚添加的课程")
def step_impl(context):
    with context.app.app_context():
        course = Courses.query.filter_by().order_by(Courses.id.desc()).first()
        req = context.client.get("/course/course/{}/".format(course.id))
    expected = context.bdd.Expected(json.loads(context.text))
    logging.info(req.json["data"])
    expected.validate(req.json["data"])


@then("'{merchant_name}'修改刚刚的课程")
def step_impl(context, merchant_name):
    with context.app.app_context():

        merchant = Merchant.query.filter_by(name=merchant_name).first()
        course = Courses.query.order_by(Courses.id.desc()).first()
        req = context.client.put(
            "/course/course/{}/".format(course.id),
            json=json.loads(context.text),
            headers={"Authorization": "JWT " + merchant.access_token},
        )
        context.bdd.is_success_request(req.json)


@when("'{merchant_name}'下架刚刚添加的课程")
def step_impl(context, merchant_name):
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=merchant_name).first()
        course = Courses.query.order_by(Courses.id.desc()).first()
        req = context.client.post(
            "/course/course/{}/".format(course.id),
            json={"status": "lower"},
            headers={"Authorization": "JWT " + merchant.access_token},
        )
    context.bdd.is_success_request(req.json)


@then("查询商户'{merchant_name}'的课程offset'{offset}'limit'{limit}'")
def step_impl(context, merchant_name, offset, limit):
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=merchant_name).first()
        req = context.client.get(
            "/course/courses/", query_string={"offset": offset, "limit": limit, "merchant_id": merchant.id}
        )
    expected = context.bdd.Expected(json.loads(context.text))
    expected.validate(req.json["data"])


@when("商户'{name}'删除最近购买课程的订单")
def step_impl(context, name):
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=name).first()
        order = Orders.query.filter(Orders.id.desc()).first()

        req = context.client.patch(
            "/course/order/{}/".format(order.id),
            json={},
            headers={"Authorization": "JWT " + merchant.access_token},
        )
    context.bdd.is_success_request(req.json)