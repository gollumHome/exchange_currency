# coding:utf-8
"""
description: 用户测试
author: jiangyx3915
date: 2019-05-25
"""


from apps.models import User, db
from test.base import BaseCase


class TestUser(BaseCase):

    @staticmethod
    def generate_users():
        user1 = User(telephone='1111111111', nickname='user1', status='normal', city='广州')
        user2 = User(telephone='1111111112', nickname='user2', status='normal', city='上海')
        user3 = User(telephone='1111111113', nickname='user3', status='normal', city='天津')
        user4 = User(telephone='1111111114', nickname='user4', status='normal', city='深圳')
        user5 = User(telephone='1111111115', nickname='user5', status='normal', city='背景')
        user6 = User(telephone='1111111116', nickname='user6', status='normal', city='厦门')
        user7 = User(telephone='1111111117', nickname='user7', status='normal', city='浙江')
        user8 = User(telephone='1111111118', nickname='user8', status='normal', city='杭州')
        user9 = User(telephone='1111111119', nickname='user9', status='normal', city='安徽')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.add(user5)
        db.session.add(user6)
        db.session.add(user7)
        db.session.add(user8)
        db.session.add(user9)
        db.session.commit()

    def setUp(self):
        super().setUp()
        self.generate_users()
        self.telephone = "19919964645"
        user = self.prepare_user(telephone=self.telephone)
        self.user_id = user.id
        merchant = self.prepare_merchant(user_id=user.id, organization_name="kkk")
        self.merchant_id = merchant.id
        self.user_headers = {"Authorization": "JWT " + user.access_token}
        self.merchant_headers = {"Authorization": "JWT " + merchant.access_token}
        admin_user = self.prepare_admin(nickname='admin')
        self.admin_user_id = admin_user.id
        self.admin_user_headers = {"Authorization": "JWT " + admin_user.access_token}

    def tearDown(self):
        self.delete_tables([User])

    def test_block_user(self):
        """
        测试封禁用户
        :return:
        """
        user = User.query.filter_by(telephone='1111111111').first()
        assert user.status == 'normal'
        response = self.client.delete(f'/platform/user/{user.id}', headers=self.admin_user_headers)
        data = response.json
        assert data["code"] == "success"
        user = User.query.filter_by(telephone='1111111111').first()
        assert user.status == 'black'

    def test_search_user(self):
        """
        测试查询用户
        :return:
        """
        # 查询名称
        rule = {
            "nickname": 'user1'
        }
        response = self.client.get('/platform/user/search?nickname=user1', headers=self.admin_user_headers)
        assert response.status_code == 200
        assert response.json['data'][0].get('telephone') == '1111111111'

    def test_update_phone(self):
        phone = "13933334444"
        response = self.client.put("/api/user/phone/", json={"phone": phone}, headers=self.user_headers)
        data = response.json
        assert data["code"] == "success"
