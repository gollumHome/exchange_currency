# -*- coding: utf-8 -*-

import time
import random

from flask_testing import TestCase

from apps import db, tc_sms, tc_oss, create_app
from apps.utils import Utils
from apps.models import Merchant, User, AdminUser, Member
from apps.auths import Auth
from config import config


class BaseCase(TestCase):
    verify_info = {}
    image_info = {}

    def hook_sender(self, phone, params, verify_type):
        self.verify_info = {"mobile": phone, "code": params[0], "minutes": params[1], "type": verify_type}
        return {"result": 0}

    def hook_upload_image(self, img_name, file_bytes):
        url = "http://%s.com" % random.choice("abcdef")
        self.image_info = {"name": img_name, "file_bytes": file_bytes, "url": url}
        return url

    @staticmethod
    def delete_tables(tables):
        for table in tables:
            db.session.query(table).delete()
        db.session.commit()

    def create_app(self):
        from celerys.tasks import celery

        celery.config_from_object(config["testing2"])
        app = create_app("testing2")
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()
        tc_sms.send_sms = self.hook_sender
        tc_oss.upload_image = self.hook_upload_image

    def prepare_user(self, telephone="15020202200"):

        user = User.query.filter_by(telephone=telephone).first()
        if not user:
            user = User(telephone=telephone, status="normal")
            db.session.add(user)
            db.session.commit()
        Auth().authenticate(user, self.app.config['USER_TOKEN_USEFUL_DATE'], self.app.config['SECRET_KEY'])
        return user

    def prepare_merchant(self, telephone="18926157202", user_id=0, **kwargs):
        args = {
            "password": Utils.set_password("123456"),
            "name": "",
            "organization_name": "",
        }
        args.update(kwargs)
        merchant = Merchant(user_id=user_id, telephone=telephone, **args)
        db.session.add(merchant)
        db.session.commit()
        merchant = Merchant.query.filter_by(telephone=telephone).first()
        Auth().authenticate_merchant(merchant, self.app.config['USER_TOKEN_USEFUL_DATE'], self.app.config['SECRET_KEY'])
        return merchant

    def prepare_admin(self, nickname="admin", password="123456"):
        admin = AdminUser(nickname=nickname, password=Utils.set_password(password))
        db.session.add(admin)
        db.session.commit()
        admin = AdminUser.query.filter_by(nickname=nickname).first()
        assert admin is not None
        Auth().authenticate_admin_user(admin, self.app.config['USER_TOKEN_USEFUL_DATE'], self.app.config['SECRET_KEY'])
        return admin

    def prepare_member(self, **kwargs):
        args = {
            "merchant_id": 0,
            "type": "gold",
            "order_id": 0,
            "status": "valid",
            "expire_time": int(time.time()) + 10086
        }
        args.update(kwargs)
        member = Member(**args)
        db.session.add(member)
        db.session.flush()
        mid = member.id
        db.session.commit()
        member = User.query.filter_by(id=mid).first()
        return member
