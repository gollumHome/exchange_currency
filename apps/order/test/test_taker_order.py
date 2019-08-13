
from apps import create_app
from flask_sqlalchemy import SQLAlchemy
import unittest
import json
from apps.models import *

app = create_app('testing')
from apps.JSONEncoder import MyJSONEncoder
app.json_encoder = MyJSONEncoder
db = SQLAlchemy(app)


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.head().__setattr__('user_id', 1)
        #db.drop_all()

    def tearDown(self):
        db.session.query(MakerOrder).delete()

    # def test_create_taker_order(self):
    #     order = db.session.query(MakerOrder).all()[0]
    #
    #     data = {
    #         'hold_currency': ECCHANGE_CURRENCY_TYPE['USD'],
    #         'hold_amount': 100,
    #         'exchange_currency':  ECCHANGE_CURRENCY_TYPE['CNY'],
    #         'book_no': order.book_no,
    #         'status':  MAKER_ORDER_STATUS['matched']
    #
    #     }
    #     resp_data = self.client.post('api/v1/order/taker_order/',  data=json.dumps(data))
    #     self.assertEqual('200', json.loads(resp_data.data)['code'])

    # def test_taker_order_list(self):
    #     resp_data = self.client.get('api/v1/order/taker_order/', )
    #     self.assertEqual('200', json.loads(resp_data.data)['code'])

    def test_update_taker_order(self):
        order = db.session.query(TakerOrder).all()[0]

        data = dict()
        data['status'] = 'matched'
        resp_data = self.client.put('api/v1/order/taker_order/?pk=%s' % order.id, data=json.dumps(data))
        self.assertEqual('200', json.loads(resp_data.data)['code'])


        # data = dict()
        # data['extend_remark'] = {'xx': "xxx"}
        # data['status'] = 'set_wallet'
        # resp_data = self.client.put('api/v1/order/taker_order/?pk=%s' % order.id, data=json.dumps(data))
        # self.assertEqual('200', json.loads(resp_data.data)['code'])
        #
        # data = dict()
        # data['status'] = 'sended'
        # resp_data = self.client.put('api/v1/order/taker_order/?pk=%s' % order.id, data=json.dumps(data))
        # self.assertEqual('200', json.loads(resp_data.data)['code'])
        #
        # data = dict()
        # data['status'] = 'received'
        # resp_data = self.client.put('api/v1/order/taker_order/?pk=%s' % order.id, data=json.dumps(data))
        # self.assertEqual('200', json.loads(resp_data.data)['code'])
        #
        # data = dict()
        # data['status'] = 'disputed'
        # resp_data = self.client.put('api/v1/order/taker_order/?pk=%s' % order.id, data=json.dumps(data))
        # self.assertEqual('200', json.loads(resp_data.data)['code'])
        #
        # data = dict()
        # data['status'] = 'complete'
        # resp_data = self.client.put('api/v1/order/maker_order/?pk=%s' % order.id, data=json.dumps(data))
        # self.assertEqual('200', json.loads(resp_data.data)['code'])
        #
        # data = dict()
        # data['status'] = 'canceled'
        # resp_data = self.client.put('api/v1/order/maker_order/?pk=%s' % order.id, data=json.dumps(data))
        # self.assertEqual('200', json.loads(resp_data.data)['code'])


if __name__ == '__main__':
    unittest.main()
