#!/usr/bin/env python
# coding: utf-8

###############################################################
#   计划执行服务类
###############################################################

import sys
import json
import logging
import datetime
# import urllib.parse
# import urllib.request
from traceback import print_exc

import requests
from dateutil.relativedelta import relativedelta
from sqlalchemy import *

from apps.models import *
from apps.utils import Utils
from apps import redis_client
from apps.order.models import *

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

logger = logging.getLogger(__name__)

# 平台结算配置
settle_config = {
    'trate_rate': 0.016,  # 1.6%的结算费率
    'recove_time': 30,  # 订单回收时间30分钟
    'recove_reward_time': 10,  # 订单回收时间10分钟,
    'enroll_timeout_time': 30  # 报名信息回收时间 10分钟
}

WX_ORDER_QUERY_URL = 'https://api.mch.weixin.qq.com/pay/orderquery'
WX_REFUND_QUERY_URL = 'https://api.mch.weixin.qq.com/pay/refundquery'
WX_TRANSFER_QUERY_URL = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/gettransferinfo'


class SchedulerApi(object):

    def __init__(self, db, tasks):
        self.db = db    # 数据库实例子
        self.tasks = tasks  # 为了避免循环引用问题，将模块变量作为参数传入

    def monitor_maker_order(self):
        taker_order_list = MakerOrder.query.filter(MakerOrder.status == 1)
        for taker_order in taker_order_list:
            if taker_order.status == '1':
                # todo redis event timeout set status
                pass
            if taker_order.status == '2':
                # todo redis event timeout set status

#
#     def recove_timeout_order(self):
#         print('recove_timeout_order time ')
#         now_time = int(time.time())
#         locked_time = settle_config['recove_time'] * 60
#         timeout_time = now_time - locked_time
#         try:
#             Orders.query.filter(and_(or_(Orders.status == 'paying', Orders.status == 'prepay'),
#                                 Orders.create_time < timeout_time)).update({Orders.status: 'canceled'})
#             self.db.session.commit()
#         except:
#             print_exc()
#         print('recove_timeout_order end ')
#
#     def trade_settle(self):
#         merchant_list = Merchant.query.filter(Merchant.status == 'normal').all()
#         if merchant_list:
#             for merchant in merchant_list:
#                 try:
#                     self._settle_step_account(merchant.id)
#                 except:
#                     print_exc()
#
#     def _settle_step_account(self, merchant_id):
#         transaction_list = Transaction.query.filter(and_(Transaction.merchant_id == merchant_id,Transaction.status == 'unsettle',
#                                                          or_(Transaction.type == 'enroll', Transaction.type == 'reward')))
#         scheduler_time = int(time.time())
#         for transaction in transaction_list:
#             settle_time = transaction.settle_time
#             subject = transaction.type
#             if scheduler_time > settle_time:
#                 amount = transaction.amount
#                 transaction_id = transaction.id
#                 order_no = transaction.order_no
#                 if subject == 'enroll':
#                     order_info = Orders.query.filter(Orders.order_no == order_no).first()
#                     if not order_info:
#                         continue
#                     enroll = Enroll.query.filter(Enroll.order_id == order_info.id).first()
#                     if not enroll:
#                         continue
#                     subject_describe = eval(str({'user_id':enroll.user_id,'activity_id': order_info.product_id, 'title':order_info.title,
#                                                 'name':enroll.full_name,'telephone':enroll.telephone,'scene':enroll.product_type}))
#
#                     book_subject = BookSubject(merchant_id=merchant_id, subject=subject, amount=amount, transaction_id=transaction_id,
#                                                subject_describe=subject_describe,create_time=scheduler_time)
#
#
#                     try:
#                         transaction.status = 'settled'
#                         order_status = order_info.status
#                         if order_status in ['refunded']:
#                             print('该订单金额不进入会计账目')
#                         else:
#                             order_info.status = 'complete'
#                             self.db.session.add(book_subject)
#                         self.db.session.commit()
#                     except:
#                         print_exc()
#                         self.db.session.rollback()
#                 elif subject == 'reward':
#                     retail_reward = RetailReward.query.filter(RetailReward.partner_trade_no == order_no).first()
#                     if not retail_reward:
#                         continue
#                     reward_user = User.query.filter(User.id == retail_reward.user_id).first()
#                     nickname, head_url, telephone = User.get_user_info(reward_user)
#                     subject_describe = eval(str({'user_id': retail_reward.user_id, 'name': nickname, 'telephone':telephone,'activity_id': retail_reward.activity_id, 'title': retail_reward.title,
#                                                  'scene': 'reward'}))
#
#                     book_subject = BookSubject(merchant_id=merchant_id, subject=subject, amount=-amount,
#                                                transaction_id=transaction_id,
#                                                subject_describe=subject_describe, create_time=scheduler_time)
#                     try:
#                         transaction.status = 'settled'
#                         self.db.session.add(book_subject)
#                         self.db.session.commit()
#                     except:
#                         print_exc()
#                         self.db.session.rollback()
#                 else:
#                     logger.info("该条流水记录异常")
#
#     def wx_order_query(self, app):
#         order_list = Orders.query.filter(Orders.status == 'paying').limit(20)
#         platform_id = int(app.config['PLATFORM_ID'])
#         for order in order_list:
#             order_no = order.order_no
#             order_type = order.order_type
#             merchant_id = order.merchant_id
#             app.logger.info('wx_order_query:::开始处理订单:::'+order_no)
#             nonce_str = Utils.get_nonce_str(Utils)
#             dict_data = {"appid": app.config['WX_APPID'], "mch_id": app.config['MERCH_ID'], "nonce_str": nonce_str,
#                          "out_trade_no": order_no}
#
#             sign = Utils.create_sign(Utils,dict_data, app.config['MERCH_KEY'])
#             dict_data['sign'] = sign
#             xml_data = Utils.dict_to_xml(Utils,dict_data)
#             try:
#                 r = requests.post(url=WX_ORDER_QUERY_URL, headers={'Content-Type': 'text/xml'},
#                                   data=xml_data.encode('utf-8'))
#                 r.encoding = 'utf-8'
#                 query_dic = Utils.xml_to_dict(r.text)
#                 # print('query_dic %s' % query_dic)
#                 return_code = query_dic['return_code']
#                 now_time = int(time.time())
#                 if return_code == 'SUCCESS':
#                     result_code = query_dic['result_code']
#                     if result_code == 'SUCCESS':
#                         trade_status = query_dic['trade_state']
#                         if trade_status == 'SUCCESS':
#                             be_verify_sign = query_dic['sign']
#                             del query_dic['sign']
#                             local_sign = Utils.create_sign(Utils,query_dic, app.config['MERCH_KEY'])
#                             if not Utils.verify_notify_sign(Utils,local_sign, be_verify_sign):  # 验证微信支付结果通知签名
#                                 logger.info('订单查询签名信息有问题--------------------')
#                                 continue
#
#                             mch_id = query_dic['mch_id']
#                             nonce_str = query_dic['nonce_str']
#                             appid = query_dic['appid']
#                             total_fee = query_dic['total_fee']
#                             out_trade_no = query_dic['out_trade_no']
#                             attach = query_dic['attach']
#                             time_end = query_dic['time_end']
#                             transaction_id = query_dic['transaction_id']
#
#                             print('wx_order_query: 系统开始处理此订单的支付状态::: %s'%out_trade_no)
#                             logger.info('wx_order_query: 系统开始处理此订单的支付状态::: ' + out_trade_no)
#                             try:
#                                 order_info = Orders.query.filter(Orders.order_no == out_trade_no).first()
#                                 # 订单信息异常
#                                 if order_info is None:
#                                     logger.info('wx_order_query: 查无此订单::: ' + out_trade_no)
#                                     continue
#
#                                 if 'payed' == order_info.status or 'complete' == order_info.status:
#                                     logger.info('wx_order_query: 系统已经处理此订单::: ' + out_trade_no)
#                                     continue
#                                 #activity = Activity.query.filter(Activity.id == product_id).first()
#
#                                 order_info.status = 'payed'
#                                 order_info.finish_time = Utils.util_settle_time(Utils,time_end, 0)
#                                 enroll = Enroll.query.filter(Enroll.order_id == order.id).first()
#                                 if enroll:
#                                     enroll.status = 'normal'
#                                 channel_pay = ChannelPay.query.filter_by(out_trade_no=out_trade_no).first()
#                                 channel_pay.mch_id = mch_id
#                                 channel_pay.attach = attach
#                                 channel_pay.transaction_id = transaction_id
#                                 channel_pay.out_trade_no = out_trade_no
#                                 channel_pay.total_fee = total_fee
#                                 channel_pay.pay_time = Utils.util_settle_time(Utils,time_end, 0)
#                                 channel_pay.status = 'success'
#
#                                 settle_time = Utils.util_settle_time(Utils,time_end, 2)  # T+1结算 结算日 1+1
#                                 transaction_type = 'enroll'
#                                 if order_type in ['member']:
#                                     transaction_type = 'member'
#                                     attach = order_info.attach
#                                     member_type = attach.get('member_type', 'silver')
#                                     member = self.create_member(member_type, merchant_id, order_info.id)
#                                     self.db.session.add(member)
#
#                                 transaction = Transaction(pay_id=str(channel_pay.id), merchant_id=merchant_id,
#                                                           order_no=out_trade_no, amount=int(total_fee), type=transaction_type,
#                                                           status='unsettle', create_time=now_time, settle_time=settle_time)
#
#                                 content = {'scene': 'attention', 'order_no': out_trade_no,
#                                            'title': order_info.title,
#                                            'img_url': order_info.img_url,
#                                            'price': order_info.price, 'shares': order_info.shares,
#                                            'amount': int(total_fee)}
#                                 content = json.dumps(content, ensure_ascii=False)
#                                 notify_message = Message(sender_id=platform_id, sender_name='校云宝',
#                                                          receiver_id=order_info.merchant_id,
#                                                          receiver_name="商户机构", message_type='notify',
#                                                          content=content,
#                                                          create_time=now_time)
#                                 # TODO:
#                                 if order_type in ['activity', 'course']:
#                                     self.tasks.async_add_reward.apply_async(args=[order_info.id],
#                                                                             queue='ADD_REWARD_QUEUE')  # 指定消息队列
#                                 self.db.session.add(notify_message)
#                                 self.db.session.add(transaction)
#                                 self.db.session.commit()
#
#                                 logger.info('wx_order_query: 系统生成一笔交易流水::: ' + 'pay_id: ' + str(channel_pay.id) + '  order_no:' +
#                                             out_trade_no + '  amount: ' + str(total_fee) + ' merchant_id: ' + str(merchant_id))
#                             except:
#                                 print_exc()
#                                 self.db.session.rollback()
#
#             except:
#                 print_exc()
#                 continue
#
#     def get_access_token(self, app):
#         try:
#             wx_session_url = app.config['WX_ACCESSTOKEN_URL']
#             params = urllib.parse.urlencode(
#                 {'appid': app.config['WX_APPID'], 'secret': app.config['WX_APP_SECRET'],
#                  'grant_type': 'client_credential'})
#             params = params.encode('utf-8')
#             with urllib.request.urlopen(wx_session_url, params, timeout=2) as f:
#                 token_data = f.read()
#                 token_data = json.loads(token_data)
#                 print('token_data %s' % token_data)
#                 if 'access_token' in token_data:
#                     access_token = token_data['access_token']
#                     expired_time = token_data['expires_in']
#                     app.config['access_token'] = access_token
#                     self.store_access_token(access_token, expired_time)
#
#         except urllib.error.URLError as e:
#             print_exc()
#         except:
#             print_exc()
#
#     def store_access_token(self, access_token, expired_time):
#         try:
#             access_token_entity = AccessToken.query.filter().first()
#             now_time = int(time.time())
#             if access_token_entity:
#                 access_token_entity.access_token = access_token
#                 access_token_entity.update_time = now_time
#                 self.db.session.commit()
#             else:
#                 access_token_entity = AccessToken(access_token=access_token, expire_in=expired_time,
#                                                   update_time=now_time)
#                 self.db.session.add(access_token_entity)
#                 self.db.session.commit()
#                 print(access_token_entity.id)
#         except:
#             print_exc()
#
#     def reward_rank(self):
#         activity_list = Activity.query.filter(Activity.status == 'active')
#         if activity_list:
#             for activity in activity_list:
#                 query = db.session.query(RetailReward.share_id,
#                                          func.sum(RetailReward.amount).label('amount'))\
#                     .filter(RetailReward.activity_id == activity.id)\
#                     .group_by(RetailReward.share_id)
#                 for x in query:
#                     reward_rank = RewardRank.query.filter(and_(RewardRank.share_id == x.share_id,
#                                                                RewardRank.activity_id == activity.id)).first()
#                     if reward_rank:
#                         reward_rank.amount = x.amount
#                     else:
#                         user = User.query.filter(User.id == x.share_id).first()
#                         if user:
#                                 rank = RewardRank(share_id=x.share_id, activity_id=activity.id, amount=x.amount,
#                                                   nickname=user.nickname, head_url=user.head_url)
#                                 self.db.session.add(rank)
#
#                     self.db.session.commit()
#
#     def complete_enrolls(self):
#         now_time = int(time.time())
#         time_out = now_time - settle_config['enroll_timeout_time']*60
#         db.session.query(Enroll).filter(and_(Enroll.status == 'unpaid', Enroll.create_time < time_out))\
#             .update({Enroll.status: 'del', Enroll.update_time: now_time})
#         self.db.session.commit()
#
#     def wx_transfers_query(self, app):
#         reward_list = RetailReward.query.filter(RetailReward.status == 'bereward').limit(30)
#         platform_id = int(app.config['PLATFORM_ID'])
#         for retail_reward in reward_list:
#             partner_trade_no = retail_reward.partner_trade_no
#             merchant_id = retail_reward.merchant_id
#             app.logger.info('wx_transfer_query:::开始处理红包奖励:::' + partner_trade_no)
#             nonce_str = Utils.get_nonce_str(Utils)
#             dict_data = {"appid": app.config['WX_APPID'], "mch_id": app.config['MERCH_ID'], "nonce_str": nonce_str,
#                          "partner_trade_no": partner_trade_no}
#
#             sign = Utils.create_sign(Utils, dict_data, app.config['MERCH_KEY'])
#             dict_data['sign'] = sign
#             xml_data = Utils.dict_to_xml(Utils, dict_data)
#             try:
#                 r = requests.post(url=WX_TRANSFER_QUERY_URL, headers={'Content-Type': 'text/xml'}, data=xml_data.encode('utf-8'),
#                                   cert=(app.config['CERT_PATH']+'/apiclient_cert.pem', app.config['CERT_PATH']+'/apiclient_key.pem'))
#                 r.encoding = 'utf-8'
#                 query_dic = Utils.xml_to_dict(r.text)
#                 # print('query_dic %s' % query_dic)
#                 return_code = query_dic['return_code']
#                 now_time = int(time.time())
#                 if return_code == 'SUCCESS':
#                     result_code = query_dic['result_code']
#                     if result_code == 'SUCCESS':
#                         transfer_status = query_dic['status']
#                         if transfer_status == 'SUCCESS':
#
#                             mch_id = query_dic['mch_id']
#                             appid = query_dic['appid']
#                             payment_amount = query_dic['payment_amount']
#                             partner_trade_no = query_dic['partner_trade_no']
#                             detail_id = query_dic['detail_id']
#                             transfer_time = query_dic['transfer_time']
#                             transfer_name = query_dic['transfer_name']
#                             payment_time = query_dic['payment_time']
#
#                             print('wx_transfer_query: 系统开始处理此红包奖励状态::: %s' % partner_trade_no)
#                             logger.info('wx_transfer_query:系统开始处理此红包奖励状态::: ' + partner_trade_no)
#                             try:
#                                 reward_info = RetailReward.query.filter(RetailReward.partner_trade_no == partner_trade_no).first()
#                                 # 订单信息异常
#                                 if reward_info:
#                                     if 'rewarded' == reward_info.status:
#                                         logger.info('wx_transfer_query: 系统已经处理此红包奖励::: ' + partner_trade_no)
#                                     else:
#                                         reward_info.status = 'rewarded'
#                                         reward_info.finish_time = Utils.str2int_time(Utils,payment_time)
#                                         content = {'scene': 'reward', 'partner_trade_no': partner_trade_no,
#                                                    'detail_id': detail_id, 'transfer_time': transfer_time,
#                                                    'payment_amount': int(payment_amount)}
#                                         content = json.dumps(content, ensure_ascii=False)
#                                         notify_message = Message(sender_id=platform_id, sender_name='校云宝',
#                                                                  receiver_id=reward_info.share_id,
#                                                                  receiver_name=transfer_name, message_type='reward',
#                                                                  content=content,
#                                                                  create_time=now_time)
#                                 else:
#                                     logger.info('wx_transfer_query: 查无此红包奖励::: ' + partner_trade_no)
#                                 # TODO:
#                                 settle_time = Utils.str2int_time(Utils,transfer_time)
#                                 transaction = Transaction(pay_id=detail_id, merchant_id=merchant_id,
#                                                           order_no=partner_trade_no, amount=int(payment_amount), type='reward',
#                                                           status='unsettle', create_time=now_time,
#                                                           settle_time=settle_time)
#                                 self.db.session.add(notify_message)
#                                 self.db.session.add(transaction)
#                                 self.db.session.commit()
#
#                                 logger.info('wx_transfer_query: 系统生成一笔红包交易流水::: ' + 'pay_id: ' + str(detail_id) +
#                                                 '  partner_trade_no:' + partner_trade_no + '  payment_amount: ' + str(payment_amount) +
#                                                 ' merchant_id: ' + str(merchant_id))
#                             except:
#                                 print_exc()
#                                 self.db.session.rollback()
#
#             except:
#                 print_exc()
#                 continue
#
#     def recove_reward_order(self):
#         print('recove_reward_order time ')
#         now_time = int(time.time())
#         locked_time = settle_config['recove_reward_time'] * 60
#         timeout_time = now_time - locked_time
#         try:
#             RetailReward.query.filter(and_(RetailReward.status == 'bereward',
#                                            RetailReward.create_time < timeout_time))\
#                 .update({Orders.status: 'canceled'})
#
#             self.db.session.commit()
#         except:
#             print_exc()
#         print('recove_reward_order end ')
#
#     @staticmethod
#     def pay_for_retail(order_id):
#         """ 这个函数是为了方便测试时替换 """
#         from celerys.tasks import async_add_reward
#         async_add_reward.apply_async(args=[order_id], queue='ADD_REWARD_QUEUE')
#
#     def complete_groups(self):
#         """
#         检查当前 groups 和 groupsWithRetail 类型的活动，如果
#             a. team 人已经满了
#             b. team 中的所有人已经支付成功
#             则成团成功，此时：
#             a. enroll 状态变为报名成功
#             b. team 状态修改为完成
#             c. 如果活动是 groupsWithRetail 类型的且有推荐人，还要向对应用户支付
#         """
#         logger.info("check_groups_team start")
#         teams = TeamGroup.query.filter_by(remain=0, status="active")\
#             .join(Activity, TeamGroup.activity_id == Activity.id)\
#             .filter(db.or_(Activity.activity_types == "groups", Activity.activity_types == "groupsWithRetail"))
#         for team in teams:
#             members = GroupMember.query.filter_by(team_id=team.id, status="normal")
#             activity = Activity.query.filter_by(id=team.activity_id).first()
#             if members.count() == team.team_limit:  # 成团
#                 for member in members:
#                     enroll = Enroll.query.filter_by(activity_id=team.activity_id, user_id=member.user_id).first()
#                     if enroll and enroll.order_id and enroll.status == "normal":
#                         if activity.activity_types == "groupsWithRetail" and member.retail_user_id:
#                             # 支付红包给 member.retail_user_id, 金额在 tasks 中生成
#                             self.pay_for_retail(enroll.order_id)
#                 team.status = "success"
#                 logger.info("Team: {team.id}, {team.chief_nickname} success")
#             else:  # 考察是否需要关闭 team
#                 activity = Activity.query.filter_by(id=team.activity_id).first()
#                 if activity.status != "active":
#                     team.status = "dead"
#                     logger.info(f"Team: {team.id}, {team.chief_nickname} dead")
#             db.session.flush()
#         db.session.commit()
#         logger.info("check_groups_team end")
#
#     def close_timeout_activity(self):
#         """
#         关闭超时的活动
#         """
#         logger.info("close_timeout_activity start")
#         now = (time.time())
#         activities = Activity.query.filter_by(status="active").filter(Activity.finish_time < now)
#         for activity in activities:
#             activity.status = "finish"
#             logger.info(f"close activity: {activity.id}, {activity.title}")
#         db.session.commit()
#         logger.info("close_timeout_activity end")
#
#     def remove_timeout_member(self, app):
#         """
#         在 groups(WithRetail) 类型的活动中
#         当单个人的支付时间超过配置时间时
#             a. enroll 状态修改为 del，如果 order 的状态是 payed/complete，发起退款（支付确认失败）
#             b. team 状态修改，释放名额
#             c. member 状态修改，失败
#         """
#         logger.info("remove_timeout_member start")
#         now = int(time.time())
#         members = GroupMember.query.filter(GroupMember.status == "unpaid",
#                                            GroupMember.update_time + (settle_config['recove_time'] + 10) * 60 < now)\
#             .join(Activity, Activity.id == GroupMember.activity_id)\
#             .filter(db.or_(Activity.activity_types == "groups", Activity.activity_types == "groupsWithRetail"))
#         logger.debug(members)
#         for member in members:
#             logger.info(f"Member: {member.id}, a: {member.activity_id}, t: {member.team_id}, {member.nickname}")
#             activity = Activity.query.filter_by(id=member.activity_id).first()
#             if activity:
#                 activity.inventory += 1
#             enroll = Enroll.query.filter_by(activity_id=member.activity_id, user_id=member.user_id)\
#                 .filter(Enroll.status != "del").first()
#             if enroll:
#                 order = Orders.query.filter_by(id=enroll.order_id).first()
#                 if order and order.status in {"payed", "complete"}:
#                     # 经过沟通，这里的退款由商家自己处理，不自动处理
#                     logger.info("should refund")
#                 # enroll.status = "del"
#             team = TeamGroup.query.filter_by(id=member.team_id).first()
#             team.members -= 1
#             if team.members == 0:
#                 team.status = "dead"
#             member.status = "del"
#             db.session.flush()
#         db.session.commit()
#         logger.info("remove_timeout_member end")
#
#     def enroll_statics(self):
#         """
#         统计更新活动的报名人数，只更新进行中的活动，完全成功视为报名成功
#         """
#         logger.info("enroll_statics start")
#         sq1 = db.session.query(Activity.id).filter_by(status="active").subquery()
#         sq2 = db.session.query(Enroll.id, Enroll.activity_id).filter(Enroll.status == "normal").subquery()
#         activity_enroll_count = db.session.query(sq1.c.id, db.func.count(sq2.c.id).label("cnt"))\
#             .outerjoin(sq2, sq1.c.id == sq2.c.activity_id)\
#             .group_by(sq1.c.id)
#         logger.debug(activity_enroll_count)
#         for activity_id, count in activity_enroll_count:
#             Activity.query.filter_by(id=activity_id).update({"enroll_count": count})
#             logger.info(f"Activity: {activity_id}, enroll count: {count}")
#         db.session.commit()
#         logger.info("enroll_statics end")
#
#     def assist_rank_job(self):
#         """
#         统计捞锦鲤排行榜
#         """
#         logger.info("assist_rank_job start")
#         share_list = ShareChain.query.filter(or_(ShareChain.activity_type == 'assist',
#                                                  ShareChain.activity_type == 'assistWithPay')).all()
#         if share_list:
#             for share_chain in share_list:
#                 share_id = share_chain.share_id
#                 activity_id = share_chain.activity_id
#                 assist_count = ShareChain.query.filter(and_(ShareChain.share_id == share_id, ShareChain.activity_id == activity_id)).count()
#                 assist_rank = AssistRank.query.filter(and_(AssistRank.share_id == share_id,AssistRank.activity_id == activity_id)).first()
#                 if not assist_rank:
#                     user = User.query.filter(User.id == share_id).first()
#                     if not user:
#                         continue
#                     enroll = Enroll.query.filter(and_(Enroll.activity_id == activity_id,
#                                                       Enroll.user_id == share_id)).first()
#                     if not enroll:
#                         continue
#                     nickname, head_url,telephone = user.get_user_info()
#                     assist_rank = AssistRank(share_id=share_id, activity_id=activity_id, assist_count=assist_count, nickname=nickname,head_url=head_url)
#                     db.session.add(assist_rank)
#                 else:
#                     activity = Activity.query.filter(Activity.id == activity_id).first()
#                     if not activity:
#                         continue
#                     status = activity.status
#                     if status in ['finish']:
#                         db.session.delete(share_chain)
#                     else:
#                         print(activity.special_params)
#                         help_max_count = activity.special_params['helper_max_count']
#                         if (assist_count >= int(help_max_count)) and (not assist_rank.finish_time):
#                             assist_rank.finish_time = int(time.time())
#                         assist_rank.assist_count = assist_count
#
#                 db.session.commit()
#                 redis_client.zdd_assist_rank(assist_count, str(share_id), str(activity_id))
#
#     def create_member(self, member_type, merchant_id,order_id):
#         now = datetime.datetime.now()
#         if member_type == "diamond":
#             delta = relativedelta(years=5)
#         elif member_type == "gold":
#             delta = relativedelta(years=3)
#         else:
#             delta = relativedelta(years=1)
#         member = Member.query.filter_by(merchant_id=merchant_id).order_by(Member.id.desc()).first()
#         if member:
#             old_expire_time = datetime.datetime.fromtimestamp(member.expire_time)
#             expire_time = max(old_expire_time, now) + delta
#         else:
#             expire_time = now + delta
#         member = Member(merchant_id=merchant_id, type=member_type, status="valid", order_id=order_id,
#                         expire_time=int(expire_time.timestamp()),create_time=int(time.time()))
#         return member
