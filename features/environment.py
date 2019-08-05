# -*- coding: utf-8 -*-
import os
import logging
import time
import tempfile
from behave import fixture, use_fixture
import features.bdd
# from apps.models import Music, Effects, db, Member, User, Merchant, Reservation, ActivityTemplate, *
from apps.models import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

os.environ.setdefault("SECRET_KEY", "dev")
app_name = os.environ.get("FLASK_CONFIG", "development2")


def decorator(func):
    """特殊的装饰,将所有client请求改成json
    """
    def _decorator(*args, **kwargs):
        print(args, kwargs)
        return func(content_type="application/json" ,*args, **kwargs)
    return _decorator


@fixture
def flaskr_client(context, *args, **kwargs):
    from apps import db, create_app

    context.app = create_app(app_name)
    context.app.testing = True
    client = context.app.test_client()
    client.put = decorator(client.put)
    client.post = decorator(client.post)
    client.get = decorator(client.get)
    client.delete = decorator(client.get)
    client.patch = decorator(client.patch)

    context.client = client
    yield context.app


def before_scenario(context, feature):
    with context.app.app_context():
        Reservation.query.delete()
        ReservationDetail.query.delete()
        Music.query.filter().delete()
        Effects.query.filter().delete()
        Courses.query.delete()
        TelVerifyCode.query.delete()
        Bargains.query.delete()
        Barrage.query.delete()
        BargainsItem.query.delete()
        EnrollSetting.query.delete()
        Enroll.query.delete()
        Activity.query.delete()
        Orders.query.delete()
        Collect.query.delete()
        AdminUser.query.delete()
        Winning.query.delete()
        WinningDetail.query.delete()
        WinningItem.query.delete()

        music = Music(
            id=1, name="稻花香", url="/static/music/1.mp3", number=1, status="normal"
        )
        db.session.add(music)
        db.session.commit()

        effects = Effects(
            id=1, name="雪花", url="/static/image/1.jpg", number=1, status="normal"
        )
        db.session.add(effects)
        db.session.commit()

        User.query.filter().delete()

        Merchant.query.filter().delete()

        # 插入活动模板
        create_activity_template()


def before_feature(context, feature):
    use_fixture(flaskr_client, context)


def before_all(context):
    context.bdd = features.bdd


def create_activity_template():
    """
    创建活动模板
    :return:
    """
    ActivityTemplate.query.delete()
    at = ActivityTemplate(id=1, name="test模板", head_diagram="/static/s.jpg")
    db.session.add(at)
    db.session.commit()
