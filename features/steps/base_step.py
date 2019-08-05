# -*- coding: utf-8 -*-
import time
import json
import logging
from behave import *
from apps.models import Music, Effects, db, Member, Merchant, User, AdminUser
from apps.auths import Auth
from datetime import timedelta
from apps.utils import Utils
import random


@given("管理员'{username}'登录系统")
def step_impl(context, username):
    admin = AdminUser(nickname=username, password=Utils.set_password(username))
    db.session.add(admin)
    db.session.commit()
    Auth().authenticate_admin_user(
        admin, context.app.config["USER_TOKEN_USEFUL_DATE"], context.app.config["SECRET_KEY"]
    )


@given("商户'{user}'登录系统")
def step_impl(context, user):
    with context.app.app_context():
        phone_dic = {"mayun": "15000000000", "liuqiangdong": "15000000001"}
        args = {
            "password": Utils.set_password("123456"),
            "name": user,
            "organization_name": "",
        }
        telephone = phone_dic.get(user, "150" + str(random.randint(11111111, 99999999)))
        user_id = 0

        merchant = Merchant(user_id=user_id, telephone=telephone, **args)
        db.session.add(merchant)
        db.session.commit()
        merchant = Merchant.query.filter_by(telephone=telephone).first()
        Auth().authenticate_merchant(
            merchant,
            context.app.config["USER_TOKEN_USEFUL_DATE"],
            context.app.config["SECRET_KEY"],
        )
        m = Merchant.query.filter_by().first()
        logging.info(m.name)


@given("用户'{user_name}'登录系统")
def step_impl(context, user_name):
    with context.app.app_context():
        phone_dic = {
            "zhangyi": "15000000001",
            "zhanger": "15000000002",
            "zhangsan": "15000000003",
        }
        telephone = phone_dic.get(
            user_name, "150" + str(random.randint(11111111, 99999999))
        )
        user = User(
            telephone=telephone,
            nickname=user_name,
            openid=1,
            head_url="/static/{}.jpg".format(user_name),
        )
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(telephone=telephone).first()
        Auth().authenticate(
            user,
            context.app.config["USER_TOKEN_USEFUL_DATE"],
            context.app.config["SECRET_KEY"],
        )
        return user


@then("得到报错信息'{error_msg}'")
def step_impl(context, error_msg):
    response = context.response
    if response["code"] != "error":
        raise Exception("不是一个错误的请求")
    context.bdd.test.assertEqual(error_msg, response["info"])


@then("返回success")
def step_impl(context):
    response = context.response
    context.bdd.is_success_request(response)
