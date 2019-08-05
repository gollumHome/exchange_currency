# -*- coding: utf-8 -*-
import json

from behave import *

from apps.models import Activity


@then("得到最近活动的弹幕")
def step_impl(context):
    with context.app.app_context():
        activity = Activity.query.order_by(Activity.id.desc()).first()
        response = context.client.get(
            "/api/activity/{}/barrage/".format(activity.id)
        )
        expected_data = json.loads(context.text)
        context.bdd.is_success_request(response.json)
        actual_data = response.json["data"]
        expected = context.bdd.Expected(expected_data)
        expected.validate(actual_data)
