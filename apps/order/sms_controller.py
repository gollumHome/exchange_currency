# coding: utf-8
from apps.tencent_sms import TencentSms
from apps.models import *
import logging
from flask import jsonify, request

logger = logging.getLogger(__name__)


class SmsController(object):
    sms_api = TencentSms()

    def send_2maker_matched(self, book_no):
        return True
        obj = MakerOrder.query.filter_by(book_no=book_no).first()
        if not obj:
            logger.info('failed, get makerorder err in book_no %s'%book_no)
            return False
        user = User.query.filter_by(user_id=obj.user_id).first()
        if not user:
            logger.info('failed, get user err in book_no=%s,user_id= %s' % (book_no,obj.user_id))
            return False
        info = 'your book_order %s'%book_no + "matched"
        sms_result = SmsController.sms_api.send_single(user.telephone, info)
        logger.info('send info to user=%s result=%s'%(obj.user_id, sms_result))
        if not sms_result:
            return False

    def send_both_disputed_info(self, book_no):

        ma_obj = MakerOrder.query.filter_by(book_no=book_no).first()
        if not ma_obj:
            logger.info('failed, get makerorder err in book_no %s' % book_no)
            return False
        ta_obj = TakerOrder.query.filter_by(book_no=book_no).first()
        if not ta_obj:
            logger.info('failed, get takerorder err in book_no %s' % book_no)
            return False
        maker_user = User.query.filter_by(user_id=ma_obj.user_id).first()
        taker_user = User.query.filter_by(user_id=ta_obj.user_id).first()
        if not maker_user and not taker_user:
            logger.info('failed, get user err in book_no=%s,user_id= %s' % (book_no))
            return False
        maker_info = 'your book_order %s' % book_no + "is beening disputed"
        taker_info = 'your book_order %s' % book_no + "is beening disputed"
        ma_sms_result = SmsController.sms_api.send_single(maker_user.telephone, maker_info)
        ta_sms_result = SmsController.sms_api.send_single(taker_info.telephone, taker_info)
        logger.info('send info to user=%s result=%s user=%s result=%s'
                                        % (maker_user.user_id, ma_sms_result,
                                        taker_user.user_id,ta_sms_result))
        if not ma_sms_result and not ta_sms_result:
            return False

    def send_2_disputed_info(self, book_no,type):
        pass

