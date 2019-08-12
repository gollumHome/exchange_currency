# -*- coding: utf-8 -*-
import time
import json
from behave import *
from apps.models import Music, Effects, db, Member, Merchant, User, Reservation, Courses
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@Then("商户'{user}'访问自己的预约页面")
def step_impl(context, user):
    logging.info(user)
    expected_data = json.loads(context.text)
    with context.app.app_context():
        user_model = Merchant.query.filter_by(name=user).first()
        response = context.client.get("/course/reservation/{}/".format(user_model.id))
    expected = context.bdd.Expected(expected_data)
    logging.info(response.json)
    expected.validate(response.json["data"])


@When("商户'{user}'设置预约页面")
def step_impl(context, user):
    logging.info(user)
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=user).first()

        response = context.client.put(
            "/course/reservation/?merchant_id={}".format(merchant.id),
            data=context.text,
            headers={"Authorization": "JWT " + merchant.access_token},
        )
    context.bdd.is_success_request(response.json)


@Then("'{user}'查看商户'{merchant}'预约页面")
def step_impl(context, user, merchant):
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=merchant).first()
        response = context.client.get("/course/reservation/{}/".format(merchant.id))

    expected_data = json.loads(context.text)
    expected = context.bdd.Expected(expected_data)
    expected.validate(response.json["data"])


@When("'{user_name}'预约商户'{merchant_name}'的课程")
def step_impl(context, user_name, merchant_name):
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=merchant_name).first()
        logging.info(context.text)
        data = json.loads(context.text)
        courses = Courses.query.filter(Courses.title.in_(data["courses"]))
        user = User.query.filter_by(nickname=user_name).first()
        c_ids = []
        for c in courses:
            c_ids.append(c.id)
        data["courses"] = c_ids
        response = context.client.post(
            "/course/reservation_detail/?merchant_id={}".format(merchant.id),
            json=data,
            headers={"Authorization": "JWT " + user.access_token},
        )

    context.bdd.is_success_request(response.json)


@Then("'{merchant_name}'查看预约")
def step_impl(context, merchant_name):
    with context.app.app_context():
        merchant = Merchant.query.filter_by(name=merchant_name).first()
        response = context.client.get(
            "/course/reservation_detail/",
            query_string=context.filter_data,
            headers={"Authorization": "JWT " + merchant.access_token},
        )
        logging.info(response)
        logging.info(context.text)
    expected_data = json.loads(context.text)
    expected = context.bdd.Expected(expected_data)
    expected.validate(response.json["data"])
