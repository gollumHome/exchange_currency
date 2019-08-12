# -*- coding: utf-8 -*-
import json
import logging
from behave import *

# logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@when("创建活动模板")
def step_impl(context):
    data = json.loads(context.text)

    response = context.client.post("/activity/activity_template/", data=data)
    logging.info(response)
    context.bdd.is_success_request(response.json)
